
import os
from celery import shared_task

# import sys
# import  django

# print(os.getcwd())
# if os.path.exists('../watch_app'):
#     sys.path.insert(0, '../watch_app')
# if os.path.exists('../'):
#     sys.path.insert(0, '../')

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mywatch.settings")
# django.setup()

from django.db.utils import DatabaseError, OperationalError
from django.db import close_old_connections


from mywatch.settings import HAARCASCADES_XML_DATA_FILE, HAARCASCADES_EXPORT_PATH
from watch_app.models import AnalysisRecord
from watch_app.parse_video import do_video_recognition


@shared_task(bind=True)
def add(self, x, y):
    print("aaa:{}".format(self.request.id))
    return x + y

@shared_task(bind=True)
def async_handler_video_recognition(self, user_id, video_upload_id, video_path, max_count):
    path_list = []
    task_id = self.request.id
    export_path = os.path.join(HAARCASCADES_EXPORT_PATH, task_id)
    os.makedirs(export_path, exist_ok=True)
    data = {
        "id": task_id,
        "upload_id": video_upload_id,
        "uid":user_id
    }
    AnalysisRecord.objects.create(**data)
    for i in HAARCASCADES_XML_DATA_FILE:
        # print(i, type(i))
        result = do_video_recognition(
            video_path=video_path, 
            cascades_data_xml=i,
            export_path=export_path,
            max_count=max_count
            )
        path_list.extend(result)
    pictures = ",".join(path_list)
    try:
        row = AnalysisRecord.objects.filter(**{"id":task_id}).update(**{"pictures":pictures, "status":1})
    except (DatabaseError, OperationalError) as e:
        print(str(e))
        close_old_connections()
        row = AnalysisRecord.objects.filter(**{"id":task_id}).update(**{"pictures":pictures, "status":1})
    print("update success:{row}".format(row=row))


if __name__ == "__main__":
    data = {
        'task_id': '4d2f450a-59c8-457f-9f99-4f19a432967e',
        'user_id': '1', 
        'video_upload_id': 3, 
        'video_path': '/Users/duanbin/work/mycat/mywatch/downloads/test_face.mp4', 
        'max_count': 20
        }
    async_handler_video_recognition(**data)