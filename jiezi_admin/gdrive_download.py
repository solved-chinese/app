from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery

from jiezi.settings import DATAFILE_SERVICE_ACCOUNT_FILE_PATH


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


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