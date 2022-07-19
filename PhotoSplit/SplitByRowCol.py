from PIL import Image
import os
import sys
import time


def get_time():
    t = time.gmtime()
    return time.strftime("%Y-%m-%d %H-%M-%S", t)


# 处理输入
def cut_img_input():
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
            row = input('输入纵向分割数量(行数)：')
        else:
            row = int(sys.argv[2])
        if row.isdigit():
            row = int(row)
            flag = True
            break
    while True:
        if len(sys.argv) < 4 or not flag:
            col = input('输入横向分割数量(列数)：')
        else:
            col = int(sys.argv[3])
        if col.isdigit():
            col = int(col)
            flag = True
            break
    img_path = img_path.replace('/', '\\')
    img_name = img_path.split('\\')[-1]
    return img_path, img_name, row, col


def cut_img():
    file_path, file_name, row_num, col_num = cut_img_input()
    img = Image.open(file_path)
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
    cut_img()
