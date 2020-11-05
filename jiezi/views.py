"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render, redirect, reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse as rest_reverse
from django.contrib.auth import logout

from learning.models import LearningProcess, StudentCharacter, StudentCharacterTag


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'unauthenticated_index.html')
    elif request.user.is_guest:
        request.user.delete()
        logout(request)
        return render(request, 'unauthenticated_index.html')
    elif request.user.is_student:
        student = request.user.student
        stats = [
            ('Last time you studied for',
             int(LearningProcess.of(student).duration_seconds // 60),
             'minutes'),
            ('You have studied for',
             int(student.total_study_duration_seconds // 60),
             'minutes'),
            ('You have seen',
             StudentCharacter.objects.exclude(
                 state=StudentCharacter.TO_LEARN).count(),
             'characters'),
        ]
        class_info = ""
        if student.in_class:
            class_info = f"You are now in {student.in_class}"
            tags = []
            for assignment in student.in_class.assignments.all():
                tags.append(StudentCharacterTag.of(student,
                                                   assignment.character_set))
        else:
            class_info = ""
            tags = StudentCharacterTag.objects.filter(student=student)
        return render(request, 'student_index.html',
                      {'stats': stats,
                       'class_info': class_info,
                       'tags': tags})
    elif request.user.is_teacher:
        return redirect(reverse('class_list'))


def about_us(request):
    return render(request, 'about_us.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    This is the root api page

    Use the OPTION request to see view permissions and available actions.
    """
    view_list = ['my_user_detail', 'search',
                 'student_character_list', 'student_character_tag_list',
                 'radical_list', 'character_list', 'character_set_list']
    view_dict = {
        view_name: rest_reverse(view_name, request=request, format=format)
        for view_name in view_list
    }
    view_dict['other_api'] = 'https://solved-chinese.github.io/api-doc/'
    return Response(view_dict)
