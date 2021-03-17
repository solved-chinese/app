import random
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models

from content.models import ReviewableObject, GeneralQuestion
from learning.models import UserReviewable, Record

MAX_REVIEW_NUM = 20


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
        can_review = bool(process.data['review_list'])
        can_learn = bool(process.data['learn_list'])
        review_cnt = len(process.data['review_list'])
        if not can_learn and not can_review:
            process.state = DoneState
        elif can_learn and not can_review:
            process.state = LearnState
        elif can_review and not can_learn:
            process.state = ReviewState
        else:
            if review_cnt < MAX_REVIEW_NUM:
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
        learn_list = process.data['learn_list']
        reviewable_pk = learn_list.pop(0)
        try:
            reviewable = ReviewableObject.objects.get(pk=reviewable_pk)
        except ReviewableObject.DoesNotExist:
            return
        # insert bonuses if applicable
        bonuses = reviewable.get_bonuses()
        for bonus in bonuses:
            ur, _ = UserReviewable.objects.get_or_create(
                user=process.user,
                reviewable=bonus
            )
            can_add_bonus = ur.learn_related(reviewable)
            if can_add_bonus:
                assert ur.bind_to_process(process)
                learn_list.insert(0, ur.reviewable.pk)
                process.data['bonus_list'].append(ur.reviewable.pk)
        process.initialize_reviewable(reviewable_pk)
        # add questions
        question_pks = list(reviewable.questions.values_list('pk', flat=True))
        process.reviewable_data(reviewable_pk)['questions'] = question_pks
        if question_pks:
            process.data['review_list'].append(reviewable_pk)
        else:
            process.data['mastered_list'].append(reviewable_pk)
        Record.objects.create(
            action=Record.Action.LEARN,
            user=process.user,
            learning_process=process,
            reviewable=reviewable,
        )
        process.state = DecideState

    @staticmethod
    def generate_response(process):
        pk2learn = process.data['learn_list'][0]
        try:
            reviewable = ReviewableObject.objects.get(pk=pk2learn)
        except ReviewableObject.DoesNotExist:
            process.data['learn_list'].pop(0)
            return DecideState.generate_response(process)
        if reviewable.word:
            # if word, assume the student has already learned
            LearnState.handle_request(process, {})
            # make it the first to review if there are questions
            if process.data['review_list'] and \
                    process.data['review_list'][-1] == reviewable.pk:
                process.data['review_list'].pop()
                process.data['review_list'].insert(0, reviewable.pk)
                process.state = ReviewState
                return ReviewState.generate_response(process)
            else:
                return DecideState.generate_response(process)
        else:
            return reviewable.render()


class RelearnState(AbstractLearningState):
    """
    relearn according to process.data['relearn_pk']
    """
    id = 'relearn'

    @staticmethod
    def handle_request(process, data):
        try:
            reviewable = ReviewableObject.objects.get(
                pk=process.data.get('relearn_pk', -1))
        except ReviewableObject.DoesNotExist:
            pass
        else:
            Record.objects.create(
                action=Record.Action.RELEARN,
                user=process.user,
                learning_process=process,
                reviewable=reviewable,
            )
        finally:
            process.state = DecideState

    @staticmethod
    def generate_response(process):
        pk2learn = process.data.get('relearn_pk', -1)
        try:
            reviewable = ReviewableObject.objects.get(pk=pk2learn)
        except ReviewableObject.DoesNotExist:
            return DecideState.generate_response(process)
        return reviewable.render()


class ReviewState(AbstractLearningState):
    """
    review the first object in review_queue
    """
    id = 'review'

    @staticmethod
    def handle_request(process, data):
        review_list = process.data['review_list']
        reviewable_pk = review_list.pop(0)
        question_list = process.reviewable_data(reviewable_pk)['questions']
        question_pk = question_list.pop(0)
        try:
            question = GeneralQuestion.objects.get(pk=question_pk)
            is_correct, correct_answer = question.check_answer(
                data.get('answer', None))
        except (GeneralQuestion.DoesNotExist, ValidationError):
            process.state = DecideState
            return {'conflict': True}
        else:
            process.data['stats']['correct_answer' if is_correct
                else 'wrong_answer'] += 1
            Record.objects.create(
                action=Record.Action.CORRECT_ANSWER if is_correct
                       else Record.Action.WRONG_ANSWER,
                user=process.user,
                reviewable=question.reviewable,
                learning_process=process,
                question=question,
                data={
                    'answer': data.get('answer', None)
                }
            )
            if is_correct:
                process.state = DecideState
            else:
                # move the question to the end of review object
                question_list.append(question_pk)
                process.data['relearn_pk'] = question.reviewable.pk
                process.state = RelearnState
            return {
                'is_correct': is_correct,
                'answer': correct_answer
            }
        finally:
            # move the review object to the end if any question left
            if question_list:
                review_list.append(reviewable_pk)
            else:
                process.data['mastered_list'].append(reviewable_pk)

    @staticmethod
    def generate_response(process):
        review_list = process.data['review_list']
        reviewable_pk = review_list[0]
        question_list = process.reviewable_data(reviewable_pk)['questions']
        random.shuffle(question_list)
        question_pk = question_list[0]
        try:
            question = GeneralQuestion.objects.get(pk=question_pk)
            render_kwargs = {}
            request = getattr(process, 'request', None)
            if request:
                render_kwargs['show_all_options'] = process.request.session.get(
                    'show_all_options', False)
            return {
                'action': 'review',
                'content': question.render(**render_kwargs)
            }
        except (GeneralQuestion.DoesNotExist, ValidationError):
            # review correct objects
            question_list.pop(0)
            if not question_list:
                review_list.pop(0)
            return DecideState.generate_response(process)


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
        self.calculate_progress_bar()
        self.save()
        response['state'] = self.state_id.hex
        response['progressBar'] = self.data['progress_bar']
        assert 'action' in response, "response invalid without action"
        return response

    def calculate_progress_bar(self):
        self.data['progress_bar'] = {
            'mastered': len(self.data['mastered_list']),
            'familiar': len(self.data['review_list']),
            'remaining': len(self.data['learn_list']),
            'bonus': len(self.data['bonus_list']),
        }

    def initialize_reviewable(self, reviewable):
        if isinstance(reviewable, ReviewableObject):
            reviewable = reviewable.pk
        self.data['reviewables'].append({'id': reviewable, 'questions': []})

    def reviewable_data(self, reviewable):
        if isinstance(reviewable, ReviewableObject):
            reviewable = reviewable.pk
        return next(item for item in self.data['reviewables']
                    if item['id'] == reviewable)

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
                'stats': {
                    'correct_answer': 0,
                    'wrong_answer': 0,
                },
                'bonus_list': [],  # list of reviewable pks, 0 is first
                'learn_list': [wis.word.get_reviewable_object().pk
                               for wis in obj.wordset.wordinset_set.all()],
                'review_list': [],
                'mastered_list': [],
                'reviewables': [],  # pk to reviewable stats
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
