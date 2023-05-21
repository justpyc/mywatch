import os
import traceback
import time

import cv2 as cv


import sys
import  django

print(os.getcwd())
if os.path.exists('../watch_app'):
    sys.path.insert(0, '../watch_app')
if os.path.exists('../'):
    sys.path.insert(0, '../')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mywatch.settings")
django.setup()

from django.db.utils import DatabaseError, OperationalError
from django.db import close_old_connections

from watch_app.models import AnalysisRecord
from watch_app.utils import get_object_or_none

def handler_time(millseconds):
    hour = 0
    minute = 0
    second = millseconds // 1000
    millsecond = millseconds % 1000

    if second > 60:
        minute = second // 60
        second = second % 60
    if minute > 60:
        hour = minute // 60
        minute = minute % 60    
    # return "{h}:{m}:{s}.{ms}".format(h=hour, m=minute, s=second, ms=millsecond)
    return hour, minute, second, millsecond

def do_video_recognition(
        video_path, 
        cascades_data_xml=None, 
        export_path=None, 
        max_count=0
        ):
    """
    video_path: 视频文件路径
    cascades_data_xml: 识别数据文件 xml路径
    export_path: 识别输出地址
    max_count: 最大识别数量
    picture_size:输出的图片尺寸
    """
    path_list = []
    if export_path is None:
        export_path = os.getcwd()
    
    video_handler = cv.VideoCapture(video_path)
    fps = video_handler.get(cv.CAP_PROP_FPS)
    
    v_width = video_handler.get(cv.CAP_PROP_FRAME_WIDTH)
    v_height = video_handler.get(cv.CAP_PROP_FRAME_HEIGHT)
    print("video fps:{s}".format(s=fps))
    print("vedio width:{}, height:{}".format(v_width, v_height))
    
    cascades_filter = cv.CascadeClassifier(cascades_data_xml)
    count = 0

    while 1:
        if count >= max_count:
            msg = "超出识别最大数量：{s}".format(s=count)
            print(msg)
            # raise RuntimeError(msg)
            return path_list
        
        ok, raw_frame = video_handler.read()
        if not ok:
            raise RuntimeError("read video failed:{s}".format(s=video_path))
         
        # height, width = raw_frame.shape[:2]
    
        # ratio = 300 / width

        # dim = (300, int(height * ratio))
        # print(ratio, dim)
        # frame = cv.resize(raw_frame, dim, interpolation=cv.INTER_AREA)

        # gray = cv.cvtColor(raw_frame, cv.COLOR_BGR2GRAY) #转为灰度图

        face_cascade = cascades_filter.detectMultiScale(
            raw_frame, scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30,30),
            flags=cv.CASCADE_SCALE_IMAGE
        
        )
        # face_cascade = cascades_filter.detectMultiScale(
        #     gray, scaleFactor=1.1, 
        #     minNeighbors=5,
        #     minSize=(30,30),
        #     flags=cv.CASCADE_SCALE_IMAGE
        
        # ) 
        # 检测人脸只接受灰度图s

        if len(face_cascade) > 0:
            millseconds = video_handler.get(cv.CAP_PROP_POS_MSEC) #获取当前帧的时间
            hour, minute, second, ms = handler_time(millseconds)
            for x, y, w, h in face_cascade:
                image = cv.resize(raw_frame, (int(v_width), int(v_height)), interpolation=cv.INTER_LINEAR)
                # image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #将图片置灰
                # image = cv.resize(image, (47, 57), interpolation=cv.INTER_CUBIC) # 处理面部大小
                image_name = "{h}h{m}min{s}s.jpg".format(h=hour, m=minute, s=second, ms=ms)
                image_path = os.path.join(export_path, image_name)
                cv.imwrite(image_path, image)
                count += 1
                # cv.imshow(image_name, image)
                path_list.append(image_path)
                print("save {c} picture to :{p}".format(c=count, p=image_path))
                # break # 每一帧只读一张脸，删除表示读取全部面积

    video_handler.release()
    cv.destoryAllWindows()
    return path_list


def video_handler(
        task_id, 
        video_path, 
        cascades_data_xml=None, 
        export_path=None, 
        max_count=0):
    status = 0
    result = []
    
    try:
        _result = do_video_recognition(video_path, cascades_data_xml, export_path, max_count)
        status = 1
        result.extend(_result)
    except Exception as e:
        error = "\n".join((traceback.format_exc(), str(e)))
        print(error) 
    obj = get_object_or_none(AnalysisRecord, **{"id":task_id})
    old_list = obj.pictures.split(",")
    result.extend(old_list)
    obj.pictures = ",".join(result)
    obj.status = status
    obj.save()

    
if __name__ == "__main__":
    xml_data = "/Users/duanbin/work/mycat/mywatch/xml_data/haarcascade_fullbody.xml"
    export_path = "/Users/duanbin/work/mycat/mywatch/tasks/afe9540d-c332-4162-af32-634875871ba9"
    # s = handler_time(8700)
    # print(s)
    res = do_video_recognition(
        "/Users/duanbin/work/mycat/mywatch/downloads/99_1684383355.mp4", 
        xml_data, export_path, 30)
    print(res)
