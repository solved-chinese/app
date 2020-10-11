"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


def index(request):
    return render(request, 'index.html')


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
