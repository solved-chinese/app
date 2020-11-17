import random

from django.db import models
from django.utils import timezone
from django_fsm import FSMIntegerField, transition, RETURN_VALUE, \
    TransitionNotAllowed

from content.models import Character
from learning.models import SCAbility, ReviewManager, Ability
from classroom.models import Assignment
from learning.constants import *


class LearningProcess(models.Model):
    # states
    DECIDE = 10
    START_LEARN = 20
    DONE_LEARN = 30
    START_RELEARN = 40
    DONE_RELEARN = 50
    TOLERANT_REVIEW_1 = 60
    TOLERANT_REVIEW_2 = 61
    TEST_REVIEW = 70
    FINISH = 80
    CHOICES = [(DECIDE, 'decide'),
               (START_LEARN, 'start_learn'),
               (DONE_LEARN, 'done_learn'),
               (START_RELEARN, 'start_relearn'),
               (DONE_RELEARN, 'done_relearn'),
               (TOLERANT_REVIEW_1, 'tolerant_review_1'),
               (TOLERANT_REVIEW_2, 'tolerant_review_2'),
               (TEST_REVIEW, 'test_review'),
               (FINISH, 'finish')]
    state = FSMIntegerField(choices=CHOICES, default=DECIDE)
    # fields
    student = models.OneToOneField('classroom.Student',
                                   on_delete=models.CASCADE,
                                   primary_key=True, related_name='+')
    review_manager = models.ForeignKey('ReviewManager',
                                       on_delete=models.PROTECT,
                                       related_name='+',
                                       default=ReviewManager.get_default_pk)
    character = models.ForeignKey(Character, related_name='+',
                                  null=True, on_delete=models.SET_NULL)
    sc_tags = models.ManyToManyField('StudentCharacterTag', related_name='+')
    review_ability = models.ForeignKey('Ability', related_name='+',
                                       null=True, on_delete=models.SET_NULL)
    review_tested_abilities = models.ManyToManyField('Ability',
                                                     related_name='+')
    # stats
    last_study_time = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=timedelta(0))

    @transition(field=state, source="*",
                target=RETURN_VALUE(TEST_REVIEW, START_LEARN, FINISH))
    def _decide(self):
        # FIXME below may be inefficient filter
        scas = SCAbility.objects.filter(
            student_character__sc_tag__in=self.sc_tags.all(),
            ability__in=self.review_manager.monitored_abilities.all(),
        )
        sca_to_learn = scas.filter(state=SCAbility.TO_LEARN).first()
        scas_to_reveiw = scas.filter(state=SCAbility.IN_PROGRESS)
        in_progress_cnt = Character.objects.filter(
            sca__in=scas_to_reveiw
        ).distinct().count()
        sca_to_review = scas_to_reveiw.get_to_review()
        if not sca_to_learn and not sca_to_review:
            return self.FINISH
        if sca_to_learn is None or in_progress_cnt >= MAX_SC_IN_PROGRESS_CNT:
            self.character = sca_to_review.character
            self.review_ability = sca_to_review.ability
            return self.TEST_REVIEW
        if in_progress_cnt < MIN_SC_IN_PROGRESS_CNT \
                or random.random() < LEARN_PROB:
            self.character = sca_to_learn.character
            return self.START_LEARN
        self.character = sca_to_review.character
        self.review_ability = sca_to_review.ability
        return self.TEST_REVIEW

    def _generate_review(self):
        if self.state == self.TOLERANT_REVIEW_1:
            review_question = self.review_manager.TOLERANT_REVIEW_1_QUESTION
        elif self.state == self.TOLERANT_REVIEW_2:
            review_question = self.review_manager.TOLERANT_REVIEW_2_QUESTION
        elif self.state == self.TEST_REVIEW:
            review_question = self.review_manager.get_review_type(
                self.review_ability.code
            )
            self.review_tested_abilities.set(
                Ability.objects.filter(code__in=review_question.test_abilities)
            )
        else:
            raise TransitionNotAllowed(f"state={self.state} is incorrect for "
                                       f"_generate_review")
        characters = Character.objects.filter(
            student_character__sc_tag__in=self.sc_tags.all())
        return 'review', {'ReviewQuestion': review_question,
                          'character': self.character,
                          'characters': characters}

    # TODO clean up
    @transition(field=state, source=START_LEARN, target=DONE_LEARN)
    def _start_learn(self):
        return 'learn', self.character

    @transition(field=state, source=DONE_LEARN, target=TOLERANT_REVIEW_1)
    def _done_learn(self):
        from learning.models import StudentCharacter
        SCAbility.objects.filter(student=self.student,
                                 character=self.character).learn_update()
        StudentCharacter.of(self.student, self.character).learn_update()

    @transition(field=state, source=START_RELEARN, target=DONE_RELEARN)
    def _start_relearn(self):
        return 'learn', self.character

    @transition(field=state, source=DONE_RELEARN, target=DECIDE)
    def _done_relearn(self):
        from learning.models import StudentCharacter
        SCAbility.objects.filter(student=self.student,
                                 character=self.character).learn_update()
        StudentCharacter.of(self.student, self.character).learn_update()

    def _finish(self):
        result = '<h2>Congrats on finishing these Character Sets:<h2>'
        for sc_tag in self.sc_tags.all():
            result += f"<h3>{sc_tag.name}</h3>"
        return None, result

    def get_action(self):
        """
        This should be called with any GET request while learning
        returns (None, None), or ('learn', character), or
        ('review', {'ReviewQuestion': review_question,
                    'character': self.character,
                    'characters': characters})
        """
        ACTIONS = {
            self.DECIDE: self._decide,
            self.START_LEARN: self._start_learn,
            self.DONE_LEARN: self._done_learn,
            self.START_RELEARN: self._start_relearn,
            self.DONE_RELEARN: self._done_relearn,
            self.TEST_REVIEW: self._generate_review,
            self.TOLERANT_REVIEW_1: self._generate_review,
            self.TOLERANT_REVIEW_2: self._generate_review,
            self.FINISH: self._finish,
        }
        for i in range(10):
            action = ACTIONS[self.state]()
            if isinstance(action, tuple):
                self._update_duration()
                self.save()
                return action
        raise Exception('InternalError: infinite loop')

    @transition(field=state, source=(TEST_REVIEW, TOLERANT_REVIEW_1,
                                     TOLERANT_REVIEW_2),
                target=RETURN_VALUE(START_RELEARN, TOLERANT_REVIEW_2, DECIDE))
    def _check_answer(self, is_correct):
        if self.state == self.TEST_REVIEW:
            from learning.models import StudentCharacter
            for ability in self.review_tested_abilities.all():
                SCAbility.of(self.student, self.character, ability).\
                    test_review_update(is_correct)
            StudentCharacter.of(self.student, self.character).\
                    test_review_update(is_correct)
            if is_correct:
                return self.DECIDE
            else:
                return self.START_RELEARN
        elif self.state == self.TOLERANT_REVIEW_1:
            return self.TOLERANT_REVIEW_2
        else: # TOLERANT_REVIEW_2
            return self.DECIDE

    def check_answer(self, is_correct):
        """
        This should be called with any POST request while learning
        :returns the correct ans_index
        """
        self._check_answer(is_correct)
        self._update_duration()
        self.save()

    def start(self, sc_tags_filter=[]):
        """
        This function resets the LearningProcess
        """
        from learning.models import StudentCharacterTag
        sc_tags = StudentCharacterTag.objects.filter_by_pk(sc_tags_filter)
        # TODO this is temporary, needs further thoughts
        assert sc_tags.count() == 1
        sc = sc_tags.get()
        cset = sc.character_set
        if self.student.in_class:
            assignment = Assignment.objects.get(
                in_class=self.student.in_class, character_set=cset)
            self.review_manager = assignment.review_manager
        sc_tags.check_update()
        self.sc_tags.set(sc_tags)
        self.state = self.DECIDE
        self.duration = timedelta(0)
        self.save()

    def reset_state(self):
        self.state = self.DECIDE
        self.save()

    def _update_duration(self):
        delta_time = timezone.now() - self.last_study_time
        if delta_time > timedelta(seconds=MAX_INTERVAL_SECONDS):
            delta_time = timedelta(seconds=MAX_INTERVAL_SECONDS)
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
