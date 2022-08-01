# -*- coding:utf-8 -*-
import math
import re
import os
import sys
import time


# 把空字符串/时间类型/时间戳(秒)转日期格式化本地时间
def format_datetime(time_item=None, format_key="%Y-%m-%d %H:%M:%S"):
    sec = 0
    if type(time_item) == time.struct_time:
        sec = int(time.mktime(time_item))
    elif time_item == "" or not time_item:
        sec = int(time.mktime(time.localtime()))
    elif type(time_item) == str or type(time_item) == float:
        sec = int(time_item)
    return time.strftime(format_key, time.localtime(sec))


# 将日期的格式的字符串转时间戳
def read_time(time_str, format_key="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(time_str, format_key)))


if __name__ == '__main__':
    stat = os.stat(r"E:\UkiyoWorkspace\dosth\demo\74.webp")
    print(stat)
    # t = time.gmtime(1643422954)
    t = time.localtime(1643422954)
    str_time = format_datetime(stat.st_ctime, "%Y-%m-%d %H:%M:%S")
    print(str_time)
    print(read_time(str_time))
    print(format_datetime())
    print(format_datetime(time.localtime()))
