"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from learning.learning_process import LearningProcess
from learning.models import StudentCharacter


def index(request):
    if not request.user.is_authenticated:
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
            ('You have ',
             StudentCharacter.of(student=student).get_in_progress_count(),
             'words in progress'),
            ('You have mastered',
             StudentCharacter.of(student=student).get_mastered_count(),
             'minutes'),
        ]
        return render(request, 'student_index.html', {'stats': stats})
    elif request.user.is_teacher:
        return render(request, 'teacher_index.html')

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
        view_name: reverse(view_name, request=request, format=format)
        for view_name in view_list
    }
    view_dict['other_api'] = 'https://solved-chinese.github.io/api-doc/'
    return Response(view_dict)
