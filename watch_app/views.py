import os
import uuid
from django.shortcuts import render, redirect
# from django.contrib.sessions.models import Session
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from watch_app.models import User, UploadRecord
from watch_app.tasks import add, async_handler_video_recognition
from watch_app.utils import get_object_or_none, my_base64_encode
from mywatch.settings import FILE_STORAGE_PATH
from pprint import pprint

# from django.contrib.auth.models import User

def login(request):
    session_key = request.session.session_key
    if session_key:
        return redirect("/watch")
    session_id = request.GET.get("session_id")
    # print("get session id:{s},".format(s=str(session_id)))
    # print("auth session:{s}".format(s=request.session.session_key))
    # if session_id is None or session_id != request.session.session_key:
    if session_id is None:
        return render(request, "login.html")
    count = User.objects.count()
    if count == 0:
        User.objects.create(**{
            "username": "admin",
            "password": my_base64_encode("123"),
            "mobile": "123456789",
            "rule":0
            }
        )
    print("user {u} login success".format(u=request.session.get("username")))
    return redirect("/watch")
    # return render(request, "index.html")

def logout(request):
    # session_id = request.session.session_key
    user_name = request.session["username"]
    # print("session_id:{s}".format(s=session_id))
    print("user:{u} logout!".format(u=user_name))
    request.session.flush()
    # sessions = Session.objects.filter(session_key=session_id)
    # print(sessions)
    # for session in sessions:
    #     print(session.__dict__)
    #     session.delete()
    # return render(request, "login.html")
    return redirect("/login")


def verfiy(request):
    data = request.POST.dict()
    username = data.get("username")
    password = data.get("password")
    user = get_object_or_none(User, **{"username": username})
    if user is None:
        return set_status_4xx(message="用户未注册：{s}".format(s=username))
    encode_passowrd = my_base64_encode(password)
    if user.password == encode_passowrd:
        result = {
            "id": user.id ,
            "username": user.username,
            "rule": user.rule
        }
        request.session["id"] = user.id
        request.session["username"] = user.username
        request.session["rule"] = user.rule
        request.session.save()
        result["sessionid"] = request.session.session_key
        return set_status_2xx(data=result)
    else:
        return set_status_4xx(message="密码错误")


def get_images(request):
    pass

def index(request):
    return render(request, "index.html")


def list_item(request):
    record = UploadRecord.objects.all()
    for i in record:
        i.location = os.path.basename(i.location)
        uid = i.uid
        user_obj = get_object_or_none(User, **{"id": uid})
        setattr(i, "username", user_obj.username)
        setattr(i, "mobile", user_obj.mobile)
    context = {"record": record}
    return render(request, "list_item.html", context)


def do_handler_vedio(request):
    data = request.POST.dict()
    # print(data)
    # {'upload_id': '1', 'location': 'compute.tgz', 'uid': '1'}
    # filename = data.get("location")
    uid = data.get("uid")
    upload_id = data.get("upload_id")
    upload_obj = get_object_or_none(UploadRecord, **{"id": int(upload_id)})
    if upload_obj is None:
        return set_status_4xx(message="没有找到文件")
    # user_obj = get_object_or_none(User, **{"id": upload_obj.uid})
    task_id = str(uuid.uuid4())
    # user_id, video_upload_id, video_path, max_count
    params = {
        "user_id": uid, 
        "video_upload_id": upload_obj.id,
        "video_path": upload_obj.location,
        "max_count":20
    }
    async_handler_video_recognition.apply_async(kwargs=params, task_id=task_id)
    return set_status_2xx(data={"task_id":"aa"})

def alert_histroy(request):
    return render(request, "alert_history.html")

def upload_file(request):
    # if request.method == "POST":
    user_id = request.session["id"]
    username = request.session["username"]
    # pprint(request.POST.dict())
    data = request.POST.dict()
    filename = data.get("name", "random.file")
    # file_name = request.FILES
    # size = request.FILES.size
    # print(request.FILES)
    stream = request.FILES["file"]
    # name = request.FILES["name"]
    file_path = os.path.join(FILE_STORAGE_PATH, filename)
    print("file path:{p}".format(p=file_path))
    handle_uploaded_file(file_path, stream)
    p = UploadRecord(**{"location":file_path, "uid": user_id})
    p.save()
    print("{u}({uid}) upload file :{p} success".format(u=username, uid=user_id, p=file_path))
    return set_status_2xx(data={"path":file_path})
        

def handle_uploaded_file(path, f):
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def set_status_2xx(data, code=200, message='success'):
    return JsonResponse({
        "code": code, "message": message, "data": data
    }, status=code)


def set_status_4xx(code=400, message='client error', data=None):
    if data is None:
        return JsonResponse({"code": code, "message": message}, status=code)
    else:
        return JsonResponse({
            "code": code, "message": message, "data": data}, status=code
        )


def set_status_5xx(code=500, message='server runtime error', data=None):
    if data is None:
        return JsonResponse({"code": code, "message": message}, status=code)
    else:
        return JsonResponse({
            "code": code, "message": message, "data": data}, status=code
        )


def test_celery(request):
    x = request.GET.get("x")
    y = request.GET.get("y")
    task_id = str(uuid.uuid4())
    add.apply_async(kwargs={"x": int(x), "y":int(y)}, task_id=task_id)
    print("create task success:{i}".format(i=task_id))
    return set_status_2xx(data=task_id)
