import io
import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from learning.models import update_from_df, Character, Radical
from .media_update_task import media_update_task
from .gdrive_download import get_service, download
from jiezi.celery import app


RADICAL_MNEMONIC_FOLDER_ID = '1_nwXyrY-q8-3xttTR9GhX8-VC0XGJLx4'
ANIMATED_STROKE_ORDER_FOLDER_ID = '1NA5KB_bU8J2Vkmnsx41FvOSMTpgfIipa'
ENTRY_FILE_ID = '1AH33mxtiev_n55fOWpUQebicLLFKaQS5aZRx93sVuJc'


@user_passes_test(lambda u: u.is_staff)
def update_entry(request):
    """ pulls entry spreadsheet from GDrive and use it to update database
    NOTE: Under current logic, it is MANDATORY that radicals are updated
    before characters """
    download_request = get_service().files().export_media(fileId=ENTRY_FILE_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    download(file, download_request)
    radical_df = pd.read_excel(file, 'Radicals')
    character_df = pd.read_excel(file, 'Characters')
    response = {'radicals': update_from_df(radical_df, Radical),
                'characters': update_from_df(character_df, Character)}
    return render(request, 'jiezi_admin/update_entry.html', response)


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
    return render(request, 'jiezi_admin/task_info.html', {'task_id': task_id})


@user_passes_test(lambda u: u.is_staff)
def kill_task(request):
    while True:
        current_task_list = list(app.control.inspect().active().values())[0]
        if current_task_list:
            task_id = current_task_list[0]['id']
            app.control.revoke(task_id, terminate=True)
        else:
            return redirect('index')
