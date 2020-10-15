import random
from datetime import timedelta

from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.db import models
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from content.models import Character
import learning.models


class LearningProcess(models.Model):
    # algorithm constants
    MAX_INTERVAL_SECONDS = 120
    DEFAULT_IN_A_ROW_REQUIRED = 2
    MAX_IN_A_ROW_REQUIRED = 2
    ADDED_DURATION = timedelta(seconds=30)
    MIN_SC_IN_PROGRESS_CNT = 3
    MAX_SC_IN_PROGRESS_CNT = 10
    LEARN_PROB = 1 / 3
    MAX_RANDOM_CHOICES = 20
    DECIDE = 10
    # states
    START_LEARN = 20
    DONE_LEARN = 30
    START_RELEARN = 40
    DONE_RELEARN = 50
    TOLERANT_REVIEW = 60
    TEST_REVIEW = 70
    FINISH = 80
    CHOICES = [(DECIDE, 'decide'),
               (START_LEARN, 'start_learn'),
               (DONE_LEARN, 'done_learn'),
               (START_RELEARN, 'start_relearn'),
               (DONE_RELEARN, 'done_relearn'),
               (TOLERANT_REVIEW, 'tolerant_review'),
               (TEST_REVIEW, 'test_review'),
               (FINISH, 'finish')]
    state = FSMIntegerField(choices=CHOICES, default=DECIDE)
    # fields
    student = models.OneToOneField('classroom.Student',
                                   on_delete=models.CASCADE,
                                   primary_key=True, related_name='+')
    character = models.ForeignKey(Character, related_name='+',
                                  null=True, on_delete=models.SET_NULL)
    sc_tags = models.ManyToManyField('learning.StudentCharacterTag',
                                     related_name='+')
    review_field_index = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True,
        validators=[MaxValueValidator(len(Character.TEST_FIELDS) - 1)]
    )
    review_answer_index = models.PositiveSmallIntegerField(default=0)
    # stats
    last_study_time = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=timedelta(0))

    @transition(field=state, source="*",
                target=RETURN_VALUE(TEST_REVIEW, START_LEARN, FINISH))
    def _decide(self):
        scs = learning.models.StudentCharacter.of(sc_tags=self.sc_tags.all())
        sc_to_learn = scs.get_one_to_learn()
        sc_to_review, self.review_field_index = scs.get_to_review()
        sc_in_progress_cnt = scs.count_all_in_progress()
        if not sc_to_review and not sc_to_learn:
            return self.FINISH
        if not sc_to_learn \
                or sc_in_progress_cnt >= LearningProcess.MAX_SC_IN_PROGRESS_CNT:
            self.character = sc_to_review.character
            return self.TEST_REVIEW
        if sc_in_progress_cnt <= LearningProcess.MIN_SC_IN_PROGRESS_CNT \
                or random.random() > LearningProcess.LEARN_PROB:
            self.character = sc_to_learn.character
            return self.START_LEARN
        self.character = sc_to_review.character
        return self.TEST_REVIEW

    def _generate_review(self):
        choices, ans_index = learning.models.StudentCharacter.of(
            student=self.student).generate_choices(
                self.character, Character.TEST_FIELDS[self.review_field_index])
        self.review_answer_index = ans_index
        question = self.character.generate_question(self.review_field_index)
        return 'review', question, choices

    @transition(field=state, source=START_LEARN, target=DONE_LEARN)
    def _start_learn(self):
        return 'learn', self.character, None

    @transition(field=state, source=DONE_LEARN, target=TOLERANT_REVIEW)
    def _done_learn(self):
        learning.models.StudentCharacter.of(self.student, self.character)\
            .learn_update()
        self.review_field_index = 0

    @transition(field=state, source=START_RELEARN, target=DONE_RELEARN)
    def _start_relearn(self):
        return 'learn', self.character, None

    @transition(field=state, source=DONE_RELEARN, target=DECIDE)
    def _done_relearn(self):
        pass

    def _finish(self):
        return None, None, None

    def get_action(self):
        """
        This should be called with any GET request while learning
        returns (None, None, None), or ('learn', character, None), or
        ('review', question, choices)
        """
        ACTIONS = {
            self.DECIDE: self._decide,
            self.START_LEARN: self._start_learn,
            self.DONE_LEARN: self._done_learn,
            self.START_RELEARN: self._start_relearn,
            self.DONE_RELEARN: self._done_relearn,
            self.TEST_REVIEW: self._generate_review,
            self.TOLERANT_REVIEW: self._generate_review,
            self.FINISH: self._finish,
        }
        for i in range(10):
            print(self.get_state_display())
            action = ACTIONS[self.state]()
            if isinstance(action, tuple):
                self.update_duration()
                self.save()
                return action
        raise Exception('InternalError: infinite loop')

    @transition(field=state, source=(TEST_REVIEW, TOLERANT_REVIEW),
                target=RETURN_VALUE(START_RELEARN, TOLERANT_REVIEW, DECIDE))
    def _check_answer(self, ans_index):
        is_correct = (ans_index == self.review_answer_index)
        print(f"answer {is_correct}")
        if self.state == self.TEST_REVIEW:
            learning.models.StudentCharacter.objects.get(
                student=self.student, character=self.character
            ).test_review_update(is_correct,
                                 Character.TEST_FIELDS[self.review_field_index])
            if is_correct:
                return self.DECIDE
            else:
                return self.START_RELEARN
        else: # we are doing tolerant_review
            self.review_field_index += 1
            if self.review_field_index == len(Character.TEST_FIELDS):
                return self.DECIDE
            return self.TOLERANT_REVIEW

    def check_answer(self, ans_index):
        """
        This should be called with any POST request while learning
        :returns the correct ans_index
        """
        print(self.get_state_display())
        self._check_answer(ans_index)
        self.update_duration()
        print(self.get_state_display())
        self.save()
        return self.review_answer_index

    def start(self, sc_tags_filter=[]):
        """
        This function resets the LearningProcess
        """
        self.sc_tags.set(
            learning.models.StudentCharacterTag.objects.filter_by_pk(
            sc_tags_filter)
        )
        self.state = self.DECIDE
        self.duration = timedelta(0)
        self.save()

    def update_duration(self):
        delta_time = timezone.now() - self.last_study_time
        if delta_time > timedelta(seconds=self.MAX_INTERVAL_SECONDS):
            delta_time = timedelta(seconds=self.MAX_INTERVAL_SECONDS)
            # TODO issue a warning like Membean
        self.duration += delta_time
        self.student.update_duration(delta_time)

    @property
    def duration_seconds(self):
        return self.duration.total_seconds()

    @classmethod
    def of(cls, student):
        """convenient get_or_create"""
        return cls.objects.get_or_create(student=student)[0]
