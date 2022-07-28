# -*- coding:utf-8 -*-
import math
import re
from PIL import Image
import os
import sys
import time
# pyinstaller -F SplitByPx.py -i split.ico --hidden-import=Pillow


# 获取当前时间并格式化
def get_time():
    t = time.gmtime()
    return time.strftime("%Y-%m-%d %H-%M-%S", t)


# 处理输入
def cut_px_img_input():
    flag = True
    while True:
        if len(sys.argv) < 2 or not flag:
            img_path = input('输入图片路径：')
            img_path = img_path.replace('\"', '')
        else:
            img_path = sys.argv[1]
        if img_path == '' or not os.path.isfile(img_path):
            num = input('文件名无效，请重新输入！[输入0退出]')
            flag = False
            if num == '0':
                exit(0)
        else:
            flag = True
            break
    while True:
        if len(sys.argv) < 3 or not flag:
            row = input('输入分割宽度的像素：')
        else:
            row = int(sys.argv[2])
        if row.isdigit():
            row = int(row)
            flag = True
            break
    while True:
        if len(sys.argv) < 4 or not flag:
            col = input('输入分割高度的像素：')
        else:
            col = int(sys.argv[3])
        if col.isdigit():
            col = int(col)
            flag = True
            break
    img_ext = img_path.split('.')[-1]
    reg_rgb = re.compile(r'jpg|jpeg|jfif|bmp|tiff|webp', re.I)
    reg_rgba = re.compile(r'png|gif|ico', re.I)
    print('可选图片格式：jpg|jpeg|jfif|bmp|tiff|webp(非透明) png|gif|ico(透明)等')
    while True:
        if len(sys.argv) < 5 or not flag:
            ext = input(f'输入分割后的图片保存格式[默认auto]【{img_ext}】：')
        else:
            ext = sys.argv[4]
        if ext == "" or ext == "auto":
            ext = img_ext
            flag = True
        ext_info = [ext, False]
        if len(reg_rgba.findall(ext)) > 0:
            ext_info[1] = True
            flag = True
            break
        elif len(reg_rgb.findall(ext)) > 0:
            flag = True
            break
        else:
            re_input = input('未知格式可能会导致分割失败！是否重新输入[y/n]？')
        if re_input == 'n' or re_input == 'N':
            flag = True
            break
    while True:
        if len(sys.argv) < 6 or not flag:
            pos = input('输入图片放置方位[N/E/W/S]【默认NE】：')
        else:
            pos = sys.argv[5]
        if pos == "":
            pos = "NE"
        if 0 < len(pos) < 3:
            flag = True
            break
    img_path = img_path.replace('/', '\\')
    img_name = img_path.split('\\')[-1]
    print('-'*20)
    return img_path, img_name, row, col, pos, ext_info


# 匹配2个方位时的正则表达式
def r(pat, string):
    reg = re.compile(r'[{0}]'.format(pat), re.I)
    res = reg.findall(string)
    if len(res) == 2:
        return True
    return False


# 获取左上角起点坐标
# 参数pos：'NEWS' 4个方位、canvas画布尺寸、image图片尺寸
def deal_align(pos, canvas, image):
    print(f'画布尺寸：{canvas[0]}x{canvas[1]}')
    print(f'原图尺寸：{image[0]}x{image[1]}')
    (cw, ch) = canvas
    (mw, mh) = image
    (x, y) = (0, 0)
    ax = mw - cw
    half_ax = ax // 2
    ay = mh - ch
    half_ay = ay // 2
    if len(pos) == 2:
        if r('NE', pos):
            (x, y) = (0, 0)
        elif r('NW', pos):
            (x, y) = (ax, 0)
        elif r('NS', pos):
            (x, y) = (0, half_ay)
        elif r('EW', pos):
            (x, y) = (half_ax, 0)
        elif r('ES', pos):
            (x, y) = (0, ay)
        elif r('WS', pos):
            (x, y) = (ax, ay)
    if len(pos) == 1:
        if r('N', pos):
            (x, y) = (half_ax, 0)
        elif r('E', pos):
            (x, y) = (0, half_ay)
        elif r('W', pos):
            (x, y) = (ax, half_ay)
        elif r('S', pos):
            (x, y) = (half_ax, ay)
        elif r('C', pos):
            (x, y) = (half_ax, half_ay)
    return x, y


# 开始分割
def cut_px_img():
    # 文件路径，文件名，分割宽度，分割高度，方位，保存后缀
    file_path, file_name, wpx, hpx, pos, ext_info = cut_px_img_input()
    [name, ext] = file_name.split('.')
    is_rgba = False
    if ext_info:
        [ext, is_rgba] = ext_info
    img = Image.open(file_path)
    width, height = img.size
    row_num = math.ceil(height/hpx)
    col_num = math.ceil(width/wpx)
    n = 0
    print(f'分割行列：{row_num}行{col_num}列')
    x, y = deal_align(pos, (col_num*wpx, row_num*hpx), (width, height))
    res_dir = f'{name}{get_time()}_{wpx}x{hpx}'
    for r in range(row_num):
        for c in range(col_num):
            box = (c*wpx + x, r*hpx + y, (c+1)*wpx + x, (r+1)*hpx + y)
            if not os.path.isdir(res_dir):
                os.mkdir(res_dir)
            split_img = img.crop(box)
            if not is_rgba:
                split_img = split_img.convert('RGB')
            else:
                split_img = split_img.convert('RGBA')
            split_img.save(f'./{res_dir}/{name}-{n}.{ext}')
            n += 1
    print('-' * 20)
    input('分割成功！文件保存在本程序所在目录的文件夹中...')


if __name__ == '__main__':
    cut_px_img()
