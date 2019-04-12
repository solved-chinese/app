import datetime
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from learning.models import update_from_df, Character, Radical


MIN_LEARN_REVIEW_INTERVAL = 30


def index(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about_us.html')

@login_required()
def start_learning(request, minutes_to_learn):
    pass

@user_passes_test(lambda u: u.is_staff)
def load_from_excel(request):
    if request.method == 'GET':
        return render(request, 'learning/load_from_excel.html')
    excel = request.FILES['excel_file']
    radical_df = pd.read_excel(excel, 'Radicals')
    character_df = pd.read_excel(excel, 'Characters')
    response = {'characters':update_from_df(character_df, Character), 'radicals':update_from_df(radical_df, Radical)}
    return render(request, 'learning/load_from_excel.html', response)