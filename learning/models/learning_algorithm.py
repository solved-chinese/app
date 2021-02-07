import random
from uuid import uuid4

from django.db import models
from rest_framework.generics import get_object_or_404

from content.models import ReviewableObject, GeneralQuestion
from learning.models import UserReviewable, Record

MAX_REVIEW_NUM = 8


class AbstractLearningState:
    """ State Pattern, context is LearningProcess """
    id = 'OVERWRITE ME'  # a string identifier for thi state

    @staticmethod
    def handle_request(process, data):
        pass

    @staticmethod
    def generate_response(process):
        pass


class DoneState(AbstractLearningState):
    id = 'done'

    @staticmethod
    def generate_response(process):
        return {
            'action': 'done'
        }


class DecideState(AbstractLearningState):
    id = 'decide'

    @staticmethod
    def generate_response(process):
        can_review = bool(process.data['review_queue'])
        can_learn = bool(process.data['learn_queue'])
        review_cnt = len(process.data['review_queue'])
        if not can_learn and not can_review:
            process.state = DoneState
        elif can_learn and not can_review:
            process.state = LearnState
        elif can_review and not can_learn:
            process.state = ReviewState
        else:
            learn_prob = max(0.0, 1 - review_cnt / MAX_REVIEW_NUM)
            learn_prob **= 2
            if random.random() < learn_prob:
                process.state = LearnState
            else:
                process.state = ReviewState
        return process.state.generate_response(process)


class LearnState(AbstractLearningState):
    """
    learns the first object in learn queue
    """
    id = 'learn'

    @staticmethod
    def handle_request(process, data):
        learn_queue = process.data['learn_queue']
        learned_pk = learn_queue.pop(0)
        learned_object = get_object_or_404(ReviewableObject, pk=learned_pk)
        # insert bonuses if applicable
        bonuses = learned_object.get_bonuses()
        for bonus in bonuses:
            ur, _ = UserReviewable.objects.get_or_create(
                user=process.user,
                reviewable=bonus
            )
            can_add_bonus = ur.learn_related(learned_object)
            if can_add_bonus:
                assert ur.bind_to_process(process)
                learn_queue.insert(0, ur.reviewable.pk)
                # record bonus
                process.data['progress_bar']['bonus'] += 1
        if learned_object.word:
            process.data['progress_bar']['remaining'] -= 1
            process.data['progress_bar']['familiar'] += 1
        # add questions if applicable
        if learned_object.questions.exists():
            process.data['review_queue'].append(
                list(learned_object.questions.values_list('pk', flat=True)))
        Record.objects.create(
            action=Record.Action.LEARN,
            user=process.user,
            learning_process=process,
            reviewable=learned_object,
        )
        process.state = DecideState

    @staticmethod
    def generate_response(process):
        pk2learn = process.data['learn_queue'][0]
        reviewable = get_object_or_404(ReviewableObject,
                                       pk=pk2learn)
        return reviewable.render()


class RelearnState(AbstractLearningState):
    """
    relearn according to process.data['relearn_pk']
    """
    id = 'relearn'

    @staticmethod
    def handle_request(process, data):
        learned_object = get_object_or_404(
            ReviewableObject, pk=process.data.get('relearn_pk', -1))
        Record.objects.create(
            action=Record.Action.RELEARN,
            user=process.user,
            learning_process=process,
            reviewable=learned_object,
        )
        process.state = DecideState

    @staticmethod
    def generate_response(process):
        pk2learn = process.data['relearn_pk']
        reviewable = get_object_or_404(ReviewableObject,
                                       pk=pk2learn)
        return reviewable.render()


class ReviewState(AbstractLearningState):
    """
    review the first object in review_queue
    """
    id = 'review'

    @staticmethod
    def handle_request(process, data):
        review_queue = process.data['review_queue']
        object_review_queue = review_queue.pop(0)
        question_pk = object_review_queue.pop(0)
        question = get_object_or_404(GeneralQuestion,
                                     pk=question_pk)
        is_correct, correct_answer = question.check_answer(
            data.get('answer', None))
        Record.objects.create(
            action=Record.Action.CORRECT_ANSWER if is_correct
                   else Record.Action.WRONG_ANSWER,
            user=process.user,
            reviewable=question.reviewable,
            learning_process=process,
            question=question,
        )
        if not is_correct:
            # move the question to the end of review object
            object_review_queue.append(question_pk)
            process.state = RelearnState
            process.data['relearn_pk'] = question.reviewable.pk
        else:
            process.state = DecideState
        # move the review object to the end if any question left
        if object_review_queue:
            review_queue.append(object_review_queue)
        elif question.reviewable.word:  # graduate this word
            process.data['progress_bar']['mastered'] += 1
            process.data['progress_bar']['familiar'] -= 1
        return {
            'is_correct': is_correct,
            'answer': correct_answer
        }

    @staticmethod
    def generate_response(process):
        random.shuffle(process.data['review_queue'][0])
        question_pk = process.data['review_queue'][0][0]
        question = get_object_or_404(GeneralQuestion,
                                     pk=question_pk)
        return {
            'action': 'review',
            'content': question.render()
        }


LEARNING_STATES = {
    state.id: state for state in
    [DoneState, DecideState, LearnState, RelearnState, ReviewState]
}


class LearningProcess(models.Model):
    user = models.ForeignKey('accounts.User',
                             on_delete=models.CASCADE)
    wordset = models.ForeignKey('content.WordSet',
                                on_delete=models.CASCADE)
    state_id = models.UUIDField(default=uuid4)
    state_type = models.CharField(max_length=20,
                                  default='decide')
    data = models.JSONField(default=dict)

    def get_response(self, data):
        response = {}
        client_state_id = data.get('state', None)  # None means new session
        if client_state_id != self.state_id.hex:
            if client_state_id is not None:
                response['conflict'] = True
        else:
            result = self.state.handle_request(self, data)
            if result:
                response.update(result)
        result = self.state.generate_response(self)
        if result:
            response.update(result)
        self.state_id = uuid4()
        self.save()
        response['state'] = self.state_id.hex
        response['progressBar'] = self.data['progress_bar'].copy()
        return response

    @classmethod
    def of(cls, user, wordset):
        obj, created = cls.objects.get_or_create(user=user, wordset=wordset)
        if created:
            obj.data = {
                'progress_bar': {
                    'mastered': 0,
                    'familiar': 0,
                    'remaining': obj.wordset.words.count(),
                    'bonus': 0,
                },
                # list of list of GeneralQuestion pks
                'review_queue': list(),
                # list of ReviewableObject pks
                'learn_queue': [
                    wis.word.get_reviewable_object().pk
                    for wis in obj.wordset.wordinset_set.all()
                ],
                'relearn_pk': -1,  # used by RelearnState
            }
            obj.save()
        return obj

    @property
    def state(self):
        return LEARNING_STATES[self.state_type]

    @state.setter
    def state(self, value):
        assert issubclass(value, AbstractLearningState)
        self.state_type = value.id

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<LP {self.pk}: {repr(self.user)}&{repr(self.wordset)}>"
