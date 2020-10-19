import io
import os
import os.path

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Radical, Character, CharacterSet
from content.media_update_task import media_update_task
from content.gdrive_download import get_service, download
from content.serializers import CharacterSerializer
from jiezi.celery import app
from jiezi.settings import MEDIA_ROOT
from .audio import get_audio
from .reviews import ReviewQuestion, AVAILABLE_REVIEW_TYPES

RADICAL_MNEMONIC_FOLDER_ID = '1boxohVl7GYOxqM1PyXKfnAMy-VP-tfvf'
ANIMATED_STROKE_ORDER_FOLDER_ID = '1D5nH3Z0rdWV3SrfY5CG8ahzXSDO0uTH-'
ENTRY_FILE_ID = '18baQLqJooho2sgfy70dybynQeXN3BiuD5_lT03EGkas'


@user_passes_test(lambda u: u.is_staff)
def update_entry(request):
    """ pulls entry spreadsheet from GDrive and use it to update database
    NOTE: Under current logic, it is MANDATORY that radicals are updated
    before characters """
    download_request = get_service().files().export_media(fileId=ENTRY_FILE_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    download(file, download_request)
    with open(os.path.join(MEDIA_ROOT, 'backup.xlsx'), 'wb') as backup:
        backup.write(file.getbuffer())
    radical_df = pd.read_excel(file, 'Radicals')
    character_df = pd.read_excel(file, 'Characters')
    cset_df = pd.read_excel(file, 'CharacterSets', index_col=0, header=None).T
    response = {}
    response['radicals'] = Radical.update_from_df(radical_df)
    response['characters'] = Character.update_from_df(character_df)
    response['character_sets'] = CharacterSet.update_from_df(cset_df)
    return render(request, 'content/update_entry.html', response)


def update_radical_mnemonic_image(request):
    return media_update(request, RADICAL_MNEMONIC_FOLDER_ID, 'Radical',
                        'mnemonic_image')


def update_character_animated_stroke_order_image(request):
   return media_update(request, ANIMATED_STROKE_ORDER_FOLDER_ID, 'Character',
                       'stroke_order_image')


@user_passes_test(lambda u: u.is_staff)
def media_update(request, folder_id, model_name, field_name):
    current_task_list = list(app.control.inspect().active().values())[0]
    if current_task_list:
        task_id = current_task_list[0]['id']
    else:
        task = media_update_task.delay(folder_id, model_name, field_name)
        task_id = task.id
    return redirect('task_info', task_id=task_id)


@user_passes_test(lambda u: u.is_staff)
def task_info(request, task_id):
    return render(request, 'content/task_info.html', {'task_id': task_id})


@user_passes_test(lambda u: u.is_staff)
def kill_task(request):
    while True:
        current_task_list = list(app.control.inspect().active().values())[0]
        if current_task_list:
            task_id = current_task_list[0]['id']
            app.control.revoke(task_id, terminate=True)
        else:
            return redirect('index')


def display_character(request, character_pk, **context_kwargs):
    """ Display character with pk=character_pk, if it is not found,
    display the next one.
    context_kwargs are passed into render directly """
    try:
        character = Character.objects.get(pk=character_pk)
    except ObjectDoesNotExist:
        character = Character.objects.filter(pk__gt=character_pk).first()
        return redirect('display_character', character_pk=character.pk)
    radicals = [character.radical_1, character.radical_2, character.radical_3]
    return render(
        request,
        'content/display_character.html',
        {'character': character, 'radicals': radicals, **context_kwargs}
    )


class Search(APIView):
    """
    This view searches all existing characters against the given `keyword`.

    Listing priority is as followed:

    1. characters with their `chinese` or unaccented `pinyin` being `keyword`
    exactly
    2. characters with their three definitions containing `keyword`

    Returns: a list of character objects with length at most 8
    """
    MAX_NUM = 8
    permission_classes = [AllowAny]

    def post(self, request):
        keyword = request.data.get('keyword', '')
        if not keyword:
            return Response([])
        characters_1 = Character.objects.filter(
            Q(pinyin__unaccent__iexact=keyword) | Q(chinese__exact=keyword)
        )
        remaining_num = max(0, self.MAX_NUM - characters_1.count())
        characters_2 = Character.objects.filter(
            Q(definition_1__icontains=keyword) |
            Q(definition_2__icontains=keyword) |
            Q(definition_3__icontains=keyword)
        ).difference(characters_1)[:]
        data = []
        for c in list(characters_1) + list(characters_2):
            data.append(CharacterSerializer(c).data)
        return Response(data)

    POST_action = {
        'keyword' : {
            'type' : 'string',
            'example' : 'hao',
        }
    }


class ReviewView(View):
    ReviewQuestion = None
    characters = None
    character = None
    answer_update = None

    def get(self, request, *args, **kwargs):
        if self.ReviewQuestion is None:
            review_type = kwargs['review_type']
            self.ReviewQuestion = AVAILABLE_REVIEW_TYPES[review_type]
        if self.character is None:
            character_pk = kwargs['character_pk']
            self.character = get_object_or_404(Character, pk=character_pk)
        correct_answer, context = self.ReviewQuestion.generate_question(
            self.character, self.characters)
        request.session['correct_answer'] = str(correct_answer)
        return render(request, self.ReviewQuestion.template, context)

    def post(self, request, *args, **kwargs):
        if self.answer_update is not None:
            self.answer_update(request.POST['user_answer'] ==
                               request.session['correct_answer'])
        return JsonResponse({'correct_answer':
                             request.session['correct_answer']})
