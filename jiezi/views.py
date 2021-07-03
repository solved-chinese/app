"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render, redirect, reverse
from django.http.response import Http404
from classroom.models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def index(request):
    return render(request, 'unauthenticated_index.html')


def about_us(request):
    return render(request, 'about_us.html')


@api_view(['GET'])
def api_root(request, format=None):
    apis = ['user-detail',
            'class-create', 'assignment-create',
            'wordset-list', 'search']
    return Response({
        api: reverse(api, request=request, format=format)
        for api in apis
    })
