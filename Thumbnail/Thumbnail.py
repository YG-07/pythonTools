# -*- coding:utf-8 -*-
import numpy as np
import cv2 as cv
import os
import math
import time
import shutil
from threading import Thread

# 打包指令 pyinstaller -F Thumbnail.py --hidden-import=opencv-python,numpy -i img.ico
# 需要手动转换的文件列表
copy_arr = []
# 压缩后的宽高
after_width = 300
after_height = 300
# 原文件夹路径
org_path = ''
# 转换失败是否复制原图
copy_flag = False

# 默认宽高
LENGTH = 300


# 获取thumb图
def get_thumb_img(file, out):
    global copy_arr
    # 读取
    # org = cv.imread(file)
    org = deal_zh_path(file)
    # 裁剪，4个点位 上下左右
    try:
        h, w = org.shape[:2]
    except AttributeError:
        print('暂时无法处理该目录的文件！')
        input('按回车键退出...')
        exit(0)
    h, w = int(h), int(w)
    dlt = int(math.fabs((w - h) / 2))
    if w > h:
        p = [0, h, dlt, dlt + h]
    else:
        p = [dlt, dlt + w, 0, w]
    spr = org[p[0]:p[1], p[2]:p[3]]
    # 缩放
    scl = cv.resize(spr, (after_width, after_height), interpolation=cv.INTER_LINEAR)
    # 保存图片
    # cv.imwrite(out, scl)
    tmp = file.split('.')
    ext = '.' + tmp.pop()
    cv.imencode(ext, scl)[1].tofile(out)
    time.sleep(0.2)


# 处理输入
def deal_input():
    global org_path
    org_path, org_fold = input_check_string("输入原图文件夹路径：")
    global after_width
    global after_height
    after_width = input_check_num("输入缩放后的宽度像素(默认300)：")
    after_height = input_check_num("输入缩放后的高度像素(默认300)：")
    global copy_flag
    copy_flag = input_yes_no('是否复制转换失败的文件？默认否(y/n)：')
    return org_fold


# 处理结束提示
def exit_tip():
    global copy_arr
    print('--------------------------------------------------------------')
    print(f'\n默认保存在本程序目录, 名为\"文件夹-th\"！')
    print('需要手动处理的文件:')
    print(copy_arr)
    input('按回车键退出...')


# 处理生成缩略图
def start_thumb_img(org_fold):
    global org_path
    out_fold = f'{org_fold}-th'
    for root, dirs, files in os.walk(org_path):
        rt = root.replace('\\', '/')
        th_rt = out_fold
        print(f'共{len(files)}个文件\n')
        print('--------------------------------------------------------------')
        if not os.path.exists(th_rt):
            os.makedirs(th_rt)
        if len(files) > 0:
            for file in files:
                file_path = f'{rt}/{file}'
                out_path = f'{th_rt}/{file}'
                ext = file.split('.').pop()
                if ext == 'gif' or ext == 'ini':
                    check_img(file_path, out_path)
                # if not os.path.exists(out_path):
                try:
                    print(file, ' 转换ing')
                    get_thumb_img(file_path, out_path)
                except cv.error:
                    check_img(file_path, out_path)


# 复制加载错误文件
def check_img(org_file, out_file):
    global copy_flag
    if not os.path.exists(out_file):
        file = org_file.split('/')[-1]
        if copy_flag:
            print(org_file, ' 复制ing')
            time.sleep(0.2)
            Thread(target=shutil.copy, args=[org_file, out_file]).start()
        else:
            print(file, '转换失败')
        copy_arr.append(file)


# 解决中文路径
def deal_zh_path(file_path):
    return cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)


# 输入并检查路径字符串
def input_check_string(msg):
    folder_path = input(msg)
    while True:
        if not folder_path == "":
            folder_path = folder_path.replace('\"', '')
            tmp = folder_path.split('\\')
            fold_name = tmp[-1]
            return folder_path, fold_name
        folder_path = input(msg)


# 输入并检查检查数字
def input_check_num(msg):
    global LENGTH
    num = input(msg)
    while True:
        if num == "":
            return LENGTH
        elif num.isdigit():
            return int(num)
        num = input(msg)


# 输入并检查y/n
def input_yes_no(msg):
    flag = input(msg)
    while True:
        if flag == "" or flag == 'n' or flag == 'N':
            return False
        elif flag == 'y' or flag == 'Y':
            return True
        flag = input(msg)


if __name__ == '__main__':
    dir_path = deal_input()
    start_thumb_img(dir_path)
    exit_tip()
