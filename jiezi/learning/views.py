from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

MIN_LEARN_REVIEW_INTERVAL = 30


def index(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about_us.html')

@login_required()
def start_learning(request, minutes_to_learn):
    pass