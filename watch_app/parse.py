# -*- coding:utf-8 -*-
import os
import math
import random

import wave
import eyed3
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

from pyAudioAnalysis import ShortTermFeatures
from pyAudioAnalysis import MidTermFeatures

# audioAnalysis.py: 主要实现了对命令行语句的执行
# MidTermFeatures, ShortTermFeatures: 实现了音频特征抽取的全部功能。包括：一共21个短期时长的特征及计算。此外，为了抽取音频特征的统计特性，也实现了一个中期时长窗口的特征计算。
# audioTrainTest.py: 实现了音频分类的过程。可以使用SVM和KNN分类器进行模型训练。此外还提供了方法的封装和常用的训练、评估、特征标准化等工具
# audioSegmentation.py: 实现了音频切割的功能，比如固定大小的分割、演讲者数字化等
# audioBasicIO.py: 主要提供了一些对音频文件的基础IO操作，如文件读取、格式转换
# audioVisualization.py: 提供了一系列功能，来把结果生成友好的和有代表性的图表

def convert_mp3_to_wav(mp3_path, export_path=None):
    if export_path is None:
        dir_name = os.path.dirname(mp3_path)
        base_name = os.path.basename(mp3_path)
        file_name = base_name.split(".")
        new_file_name = "{}.wav".format(file_name[0])
        export_path = os.path.join(dir_name, new_file_name)

    stream = AudioSegment.from_file(mp3_path, format="mp3")
    stream.export(export_path, format="wav")
    return export_path




if __name__ == "__main__":
    mp3_path = "/opt/mywatch/alert/0.mp3"
    # wav_path = convert_mp3_to_wav(mp3_path)
    # print(wav_path)
    mp3_dir = "/opt/mywatch/alert"
    wav_dir = "/opt/mywatch/alert_wav"
    _list = os.listdir(mp3_dir)
    for i in _list:
        p = os.path.join(mp3_dir, i)
        tmp = i.split(".")
        new_file_name = "{}.wav".format(tmp[0])
        w = os.path.join(wav_dir, new_file_name)
        r = convert_mp3_to_wav(p, w)
        print("{} -> {}".format(p, w))

