import pandas as pd
from PIL import Image
from apiclient import discovery
import os
import io
import html

from celery import shared_task, task, Task
from celery_progress.backend import ProgressRecorder

from jiezi.settings import MEDIA_ROOT
import learning.models
from .gdrive_download import get_service, download


@shared_task(bind=True)
def media_update_task(self, folder_id, model_name, field_name):
    print('starting')
    progress_recorder = ProgressRecorder(self)
    Model = getattr(learning.models, model_name)
    msg = '-----------------<br>' \
          + html.escape(f'PROGRESS REPORT ON UPDATE OF {field_name} of {Model.__name__}s') \
          + '<br>-----------------<br>'
    service = get_service()

    models = Model.objects.all()
    num_models = len(models)
    for index, model in enumerate(models):
        jiezi_code = repr(model)[1:6]
        list = service.files().list(
            pageSize=1000,
            q=f"mimeType contains 'image/' "
              f"and '{folder_id}' in parents "
              f"and name contains '{jiezi_code}'"
        ).execute()
        if len(list['files']) != 1:
            err = '<br><div style="color:red;">'\
                  + html.escape(f'ERR: Expect 1 image of {model} '
                    f'but get {len(list["files"])} images') \
                  + "</div>"
            print(err)
            msg += err
            setattr(model, field_name, 'default.jpg')
            model.save()
        else:
            file = list['files'][0]
            path = os.path.join(MEDIA_ROOT, field_name, file['name'])
            download_request = service.files().get_media(fileId=file['id'])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file = io.FileIO(path, mode='w')
            download(file, download_request)
            setattr(model, field_name,
                    os.path.join(field_name, os.path.basename(path)))
            model.save()
            info = '<span style="color:green;">' \
                   + html.escape(f"OK: {model}") \
                   + f'<img src="{getattr(model, field_name).url}" style="width:50px;height:50px;display: inline-block;">' \
                   + '</span>'
            print(info)
            msg += info
        progress_recorder.set_progress(index, num_models, description=msg)

        # if is_make_square:
        #     img = Image.open(path)
        #     img = img.resize((600, 600), Image.ANTIALIAS)
        #     img.save(path, optimize=True, quality=80)


