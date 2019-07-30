"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about_us.html')


def the_science_behind(request):
    return render(request, 'the_science_behind.html')


def help(request):
    return render(request, 'help.html')
