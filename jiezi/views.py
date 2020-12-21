"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render, redirect, reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse as rest_reverse
from django.contrib.auth import logout


def index(request):
    return render(request, 'unauthenticated_index.html')


def about_us(request):
    return render(request, 'about_us.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    This is the root api page

    Use the OPTION request to see view permissions and available actions.
    """
    view_list = ['my_user_detail']
    view_dict = {
        view_name: rest_reverse(view_name, request=request, format=format)
        for view_name in view_list
    }
    view_dict['other_api'] = 'https://solved-chinese.github.io/api-doc/'
    return Response(view_dict)
