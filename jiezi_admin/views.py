import io

import pandas as pd
from apiclient import discovery
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from jiezi.settings import DATAFILE_SERVICE_ACCOUNT_FILE_PATH
from learning.models import update_from_df, Character, Radical


SCOPES = ['https://www.googleapis.com/auth/drive']
RADICAL_MNEMONIC_FOLDER_ID = '1_nwXyrY-q8-3xttTR9GhX8-VC0XGJLx4'
COLOR_CODED_CHARACTER_FOLDER_ID = '1BCKiQx0dUAnwSOffgLPrXoSFsi8OQzxZ'
ANIMATED_STROKE_ORDER_FOLDER_ID = '1NA5KB_bU8J2Vkmnsx41FvOSMTpgfIipa'
ENTRY_FILE_ID = '1AH33mxtiev_n55fOWpUQebicLLFKaQS5aZRx93sVuJc'


def get_service():
    credentials = service_account.Credentials.from_service_account_file(
        DATAFILE_SERVICE_ACCOUNT_FILE_PATH, scopes=SCOPES)
    service = discovery.build('drive', 'v3', credentials=credentials)
    return service


def download(file, download_request):
    downloader = MediaIoBaseDownload(file, download_request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()


@user_passes_test(lambda u: u.is_staff)
def update_entry(request):
    download_request = get_service().files().export_media(fileId=ENTRY_FILE_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    download(file, download_request)
    radical_df = pd.read_excel(file, 'Radicals')
    character_df = pd.read_excel(file, 'Characters')
    response = {'radicals': update_from_df(radical_df, Radical),
                'characters': update_from_df(character_df, Character)}
    return render(request, 'learning/load_from_excel.html', response)


def test_authenticate(request):
    service = get_service()
    # list = service.files().list(pageSize=1000).execute()
    download_request = service.files().export_media(fileId=ENTRY_FILE_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    download(file, download_request)

