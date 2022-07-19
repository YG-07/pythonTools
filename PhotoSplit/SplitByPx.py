import math

from PIL import Image
import os
import sys
import time

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
            num = input('文件名无效！输入0退出')
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
    img_path = img_path.replace('/', '\\')
    img_name = img_path.split('\\')[-1]
    return img_path, img_name, row, col


def deal_align(pos, canvas, image):
    (cw, ch) = canvas
    (mw, mh) = image
    (x, y) = (0, 0)
    ax = mw - cw
    half_ax = (mw - cw) // 2
    ay = mh - ch
    half_ay = (mh - ch) // 2
    if pos.find('N'):
        if len(pos) == 1:
            x = half_ax
        elif pos.find('W'):
            x = ax
        elif pos.find('S'):
            y = half_ay
    if pos.find('E'):
        if len(pos) == 1:
            y = half_ay
        elif pos.find('W'):
            x = half_ax
        elif pos.find('S'):
            y = ay
    if pos.find('S'):
        if len(pos) == 1:
            (x, y) = (half_ax, ay)

    if pos.find('W'):
        if len(pos) == 1:
            (x, y) = (ax, half_ay)
    return x, y


def cut_px_img():
    # 文件路径，文件名，分割宽度，分割高度
    file_path, file_name, wpx, hpx = cut_px_img_input()
    img = Image.open(file_path)
    [name, ext] = file_name.split('.')
    width, height = img.size
    print(width, height)
    row_num = math.ceil(height/hpx)
    col_num = math.ceil(width/wpx)
    n = 0
    print(row_num, col_num)
    res_dir = f'{name}{get_time()}_{wpx}x{hpx}'
    for r in range(row_num):
        for c in range(col_num):
            box = (c*wpx, r*hpx, (c+1)*wpx, (r+1)*hpx)
            if not os.path.isdir(res_dir):
                os.mkdir(res_dir)
            img.crop(box).save(f'./{res_dir}/{name}-{n}.{ext}')
            n += 1
    input('分割并保存成功...')


if __name__ == '__main__':
    cut_px_img()