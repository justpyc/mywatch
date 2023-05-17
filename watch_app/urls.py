from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("", views.index, name="index"),
    path("identify-history", views.list_item, name="list_item"),
    path("list-task-record", views.list_task_record, name="list-task-record"),
    path("list-user-favour", views.list_user_favour, name="list-task-record"),
    path("api/v1/get-user-favour", views.get_user_favour, name="get-user-favour"),
    path("upload-file", views.upload_file, name="upload-file"),
    path('api/v1/verfiy', views.verfiy, name='verfiy'),
    path('api/v1/handler-video', views.do_handler_vedio, name="do-handler-vedio"),
    path('api/v1/get-task-info', views.get_task_info, name="get-task-info"),
    path('api/v1/create-user-favour', views.create_user_favour, name="create-user-favour"),
    path('api/v1/add', views.test_celery, name="test-celery"),
    path('image', views.get_images, name="get-images"),
    path('video', views.play_video, name="play-video"),
]
