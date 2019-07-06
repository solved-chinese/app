import io
import os
from tqdm import tqdm

import pandas as pd
from PIL import Image
from apiclient import discovery
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import user_passes_test

from jiezi.settings import DATAFILE_SERVICE_ACCOUNT_FILE_PATH, MEDIA_ROOT
from learning.models import update_from_df, Character, Radical


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
RADICAL_MNEMONIC_FOLDER_ID = '1_nwXyrY-q8-3xttTR9GhX8-VC0XGJLx4'
COLOR_CODED_CHARACTER_FOLDER_ID = '1BCKiQx0dUAnwSOffgLPrXoSFsi8OQzxZ'
ANIMATED_STROKE_ORDER_FOLDER_ID = '1NA5KB_bU8J2Vkmnsx41FvOSMTpgfIipa'
ENTRY_FILE_ID = '1AH33mxtiev_n55fOWpUQebicLLFKaQS5aZRx93sVuJc'


def _get_service():
    credentials = service_account.Credentials.from_service_account_file(
        DATAFILE_SERVICE_ACCOUNT_FILE_PATH, scopes=SCOPES)
    service = discovery.build('drive', 'v3', credentials=credentials)
    return service


def _download(file, download_request):
    downloader = MediaIoBaseDownload(file, download_request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()


@user_passes_test(lambda u: u.is_staff)
def update_entry(request):
    """ pulls entry spreadsheet from GDrive and use it to update database
    NOTE: Under current logic, it is MANDATORY that radicals are updated
    before characters """
    download_request = _get_service().files().export_media(fileId=ENTRY_FILE_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    _download(file, download_request)
    radical_df = pd.read_excel(file, 'Radicals')
    character_df = pd.read_excel(file, 'Characters')
    response = {'radicals': update_from_df(radical_df, Radical),
                'characters': update_from_df(character_df, Character)}
    return render(request, 'jiezi_admin/update_entry.html', response)


def _update_media(log_file, parent_id, Model, field_name, is_make_square=False):
    """ update an ImageField of a model, making it square if necessary
    Args:
        log_file (file): the log file to write to
        parent_id (str): the id of the parent folder
        Model (Model): the model class
        field_name (str): the name of the ImageField to update
        is_make_square (bool): whether to make the image (default: False)
    """
    log_file.write(f'-----\n-----\nnow updating {field_name}-----\n-----\n')
    service = _get_service()
    for model in tqdm(Model.objects.all()):
        name = str(model)
        jiezi_id = name.split(':')[0]
        list = service.files().list(pageSize=1000, q=f"mimeType contains 'image/' \
            and '{parent_id}' in parents and name contains '{jiezi_id}'").execute()
        if len(list['files']) != 1:
            err = f"ERR: Expect 1 image of {name} but get {len(list['files'])} \n"
            log_file.write(err)
            print(err)
            setattr(model, field_name, 'default.jpg')
            model.save()
            continue
        file = list['files'][0]
        path = os.path.join(MEDIA_ROOT, field_name, file['name'])
        download_request = service.files().get_media(fileId=file['id'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = io.FileIO(path, mode='w')
        _download(file, download_request)

        if is_make_square:
            img = Image.open(path)
            img = img.resize((600, 600), Image.ANTIALIAS)
            img.save(path, optimize=True, quality=80)

        setattr(model, field_name, os.path.join(field_name, os.path.basename(path)))
        model.save()


@user_passes_test(lambda u: u.is_staff)
def update_media(request):
    """ Note: due to performance issues, only one instance of this function can
    be run at the same time. This is done by allowing the program to proceed
    only if 'media/lock' doesn't exist. """
    if os.path.exists('media/lock'):
        return HttpResponse('Media is being updated, it is supposed to \
        take 20 minutes. Come back later.')
    with open('media/lock', 'w') as f:
        f.write('lock')
    try:
        with open('media/log', 'w') as f:
            list = [
                [RADICAL_MNEMONIC_FOLDER_ID, Radical, 'mnemonic_image', True],
                [COLOR_CODED_CHARACTER_FOLDER_ID, Character, 'color_coded_image'],
                [ANIMATED_STROKE_ORDER_FOLDER_ID, Character, 'stroke_order_image'],
            ]
            for row in list:
               _update_media(f, *row)
            return redirect(media_update_status)
    finally:
        os.remove('media/lock')


@user_passes_test(lambda u: u.is_staff)
def media_update_status(request):
    if os.path.exists('media/lock'):
        return HttpResponse('Media is being updated, it is supposed to take \
                   20 minutes. Come back later.')
    else:
        with open('media/log', 'r') as f:
            return HttpResponse(f.read(), content_type="text/plain; charset=utf-8;")
