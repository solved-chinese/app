import pandas as pd
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ObjectDoesNotExist

from learning.models import update_from_df, Character, Radical, Report
from accounts.models import User


def display_character(request, character_pk):
    try:
        character = Character.objects.get(pk=character_pk)
    except ObjectDoesNotExist:
        character = Character.objects.filter(pk__gt=character_pk).first()
        return redirect('display_character', character_pk=character.pk)

    character = Character.objects.filter(pk__gte=character_pk).first()
    radicals = [Radical.objects.get(pk=character.radical_1_id)]
    radicals.append(Radical.objects.get(pk=character.radical_2_id)
                    if character.radical_2_id else None)
    radicals.append(Radical.objects.get(pk=character.radical_3_id)
                    if character.radical_3_id else None)
    return render(request, 'learning/display_character.html',
                  {'character':character, 'radicals':radicals})


@login_required()
def start_learning(request, minutes_to_learn):
    if request.user.last_study_date == timezone.now().date() - datetime.timedelta(days=1):
        request.user.study_streak += 1
    else:
        request.user.study_streak = 1
    request.user.last_study_date = timezone.now().date()
    request.user.last_study_time = timezone.now()
    request.user.last_study_duration = datetime.timedelta(seconds=0)
    request.user.save()

    request.session['last_record_time'] = timezone.now()
    request.session['is_learning'] = True
    request.session['end_learning_time'] = timezone.now() + \
        datetime.timedelta(minutes=minutes_to_learn)


@login_required()
def learning_process(request):
    """To be implemented"""
    delta_time = timezone.now() - request.session['last_record_time']
    request.session['last_record_time'] = timezone.now()
    request.user.last_study_duration += delta_time
    request.user.total_study_duration += delta_time
    request.user.last_study_time = timezone.now()
    request.user.save()

    if request.session['end_learning_time'] > timezone.now():
        return end_learning(request)


@login_required()
def end_learning(request):
    return render(request, 'simple_response.html', {
        'content': 'You are finished.'
    })


def report(request):
    try:
        report = Report(origin=request.POST.get('origin'),
                        description_1=request.POST.get('description_1'),
                        description_2=request.POST.get('description_2'))
        if isinstance(request.user, User):
            report.user = request.user
        report.save()
        return render(request, 'simple_response.html', {
            'content':'Thank you for your response!'
        })
    except:
        return render(request, '404.html')
