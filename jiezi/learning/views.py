import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from learning.models import update_from_df, Character, Radical, Report
from accounts.models import User


def index(request):
    # because the index page isn't ready
    return redirect('/learning/C0001')


def display_character(request, character_pk):
    character = Character.objects.get(pk=character_pk)
    radicals = [Radical.objects.get(pk=character.radical_1_id)]
    radicals.append(Radical.objects.get(pk=character.radical_2_id)
                    if character.radical_2_id else None)
    radicals.append(Radical.objects.get(pk=character.radical_3_id)
                    if character.radical_3_id else None)
    return render(request, 'learning/display_character.html',
                  {'character':character, 'radicals':radicals})


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
    response = {'radicals':update_from_df(radical_df, Radical)}
    response['characters'] = update_from_df(character_df, Character)
    return render(request, 'learning/load_from_excel.html', response)


def report(request):
    try:
        report = Report(origin=request.POST.get('origin'),
                        description_1=request.POST.get('description_1'),
                        description_2=request.POST.get('description_2'))
        if isinstance(request.user, User):
            report.user = request.user
        report.save()
        return render(request, 'simple_response.html', {'content':'Thank you for your response!'})
    except:
        return render(request, '404.html')
    