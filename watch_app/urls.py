from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("", views.index, name="index"),
    path("identify-history", views.list_item, name="list_item"),
    path("alert-history", views.list_task_record, name="list-task-record"),
    path("upload-file", views.upload_file, name="upload-file"),
    path('api/v1/verfiy', views.verfiy, name='verfiy'),
    path('api/v1/handler-video', views.do_handler_vedio, name="do-handler-vedio"),
    path('api/v1/get-task-info', views.get_task_info, name="get-task-info"),
    path('api/v1/add', views.test_celery, name="test-celery"),
    path('image', views.get_images, name="get-images"),
]
