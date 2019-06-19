"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')