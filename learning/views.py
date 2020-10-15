import json
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from accounts.models import User
from classroom.models import Student
from content.models import CharacterSet
from content.views import display_character
from jiezi.rest.permissions import IsStudent, IsNotGuest
from .models import StudentCharacterTag, Report
from learning.learning_process import LearningProcess
from jiezi.utils.mixins import RegisteredStudentOnlyMixin


@login_required
def manage_library(request, set_id=None):
    if set_id:
        context = {'set': StudentCharacterTag.objects.get(pk=set_id)}
        return render(request, 'learning/manage_set.html', context)
    return render(request, 'learning/manage_library.html')


def try_me(request):
    if request.user.is_authenticated:
        return redirect('')
    user = User.objects.create_guest_student()
    student = Student.of(user)
    login(request, user)
    try_me_set = CharacterSet.objects.get(name='try_me')
    obj = StudentCharacterTag.objects.create(character_set=try_me_set,
                                             student=student)
    obj.update_from_character_set()
    process = LearningProcess.of(request.user.student)
    process.start([obj.pk])
    return redirect(reverse('continue_learning'))


class StartLearning(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, sc_tags_filter=None):
        student = request.user.student

        if not sc_tags_filter:
            sc_tags_filter = json.loads(request.data.get('sc_tags_filter', None))

        assert isinstance(sc_tags_filter, list), 'sc_tags_filter must be ' \
                                                 'list of ints'
        for sc_tag in sc_tags_filter:
            assert StudentCharacterTag.objects.get(pk=sc_tag).student \
                   == student
        LearningProcess.of(student).start(sc_tags_filter)
        return redirect(reverse('continue_learning'))


class Learning(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get_learning_process(self, request):
        student = self.request.user.student
        return LearningProcess.of(student)

    def finish(self, request):
        return render(request, 'utils/simple_response.html', {
            'content': 'Congrats on finishing these Character Sets!'
        })

    def review(self, request, question, choices):
        return render(request, 'learning/review.html', {
            'question': question,
            'choices': choices,
        })

    def get(self, request):
        process = self.get_learning_process(request)
        mode, data_1, data_2 = process.get_action()
        if mode is None:
            return self.finish(request)
        elif mode == 'learn': # character, None
            return display_character(request, data_1.pk, is_next=True)
        elif mode == 'review': # question, choices
            return self.review(request, data_1, data_2)

    def post(self, request):
        # used for checking answer only
        process = self.get_learning_process(request)
        ans_index = int(request.data['user_answer'])
        ans_index = process.check_answer(ans_index)
        return Response({'correct_answer':ans_index},
                        status=status.HTTP_200_OK)

"""
@api {POST} /learning/start_learning/  Start Learning
@apiDescription Start Learning, this should be done with an actual form submission
@apiGroup learning

@apiParam  {int[]}   uc_tags_filter the ids of UserCharacterTags to INCLUDE


@apiSuccessExample learning/review.html
context dictionary:
'choices': a list of 4 strings
'question': string of the question

Display the question and choices with no next button
After the user selects an answer, ajax POST to the same url with following args:
    'user_answer': integer with range [0, 4), representing user's answer
The server responds with 'correct_answer', which is in the same range,
    display the result, provide next button, and when the user clicks next, 
    submit GET request with no args
refer to old master review page for how to do specific things
    https://github.com/chenyx512/jiezi/blob/old-master/jiezi/templates/learning/review_interface.html

@apiSuccessExample learning/display_character.html:
There shouldn't be any ajax in this
In context dictionary, if 'is_next', provide an next button that submits
    GET form to original url, otherwise keep the next button the same as before
"""

def report(request):
    report = Report(origin=request.POST.get('origin'),
                    description_1=request.POST.get('description_1'),
                    description_2=request.POST.get('description_2'))
    if isinstance(request.user, User):
        report.user = request.user
    report.save()
    return render(request, 'utils/simple_response.html', {
        'content': 'Thank you for your response!'
    })
