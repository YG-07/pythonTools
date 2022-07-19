from PIL import Image
import os
import sys
import time


def get_time():
    t = time.gmtime()
    return time.strftime("%Y-%m-%d %H-%M-%S", t)


# 处理输入
def cut_img_input():
    if len(sys.argv) < 2:
        img_name = input('输入文件名：')
    else:
        img_name = sys.argv[1]
    if img_name == '' or not os.path.isfile(img_name):
        input('文件名无效！')
        exit(0)
    row = input('输入纵向分割数量(行数)：')
    col = input('输入横向分割数量(列数)：')
    if row == '':
        row = 1
    else:
        row = int(row)
    if col == '':
        col = 1
    else:
        col = int(col)
    return img_name, row, col


def cut_img():
    file_name, row_num, col_num = cut_img_input()
    img = Image.open(file_name)
    [name, ext] = file_name.split('.')
    width, height = img.size
    w = width//col_num
    h = height//row_num
    n = 0
    res_dir = f'{name}{get_time()}_{row_num}x{col_num}'
    for r in range(row_num):
        for c in range(col_num):
            box = (c*w, r*h, (c+1)*w, (r+1)*h)
            if not os.path.isdir(res_dir):
                os.mkdir(res_dir)
            img.crop(box).save(f'./{res_dir}/{name}-{n}.{ext}')
            n += 1
    input('分割并保存成功...')


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    os.chdir(path)
    cut_img()