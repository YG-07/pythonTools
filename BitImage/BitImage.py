# -*- coding:utf-8 -*-
import math
import os
import time
import requests
from PIL import Image
import numpy as np
# pyinstaller -F BitImage.py -i broken.ico --hidden-import=Pillow,numpy,requests,os


# 不足补充特定字符
def str_fill(org, lg, char):
    n = math.ceil((lg - len(org)) / len(char))
    res = char * n + org
    return res


# bytes转ASCII,ASCII码转二进制
def str_to_bin(info_str):
    arr = []
    try:
        bin_str = info_str.encode('utf-8')
    except AttributeError:
        bin_str = info_str
    for i in range(len(bin_str)):
        tmp = bin(bin_str[i]).replace('0b', '')
        tmp = str_fill(tmp, 8, '0')
        arr.append(tmp)
    return arr


# 生成ndarray数组，并保存图片
def array_to_image(array, path):
    al = len(array)
    row = math.ceil(al/32)
    nd_arr = np.zeros([row, 256, 3], dtype=np.uint8)
    r = 0
    c = 0
    for i in range(al):
        for j in range(8):
            ch = array[i][j]
            # 1代表一个黑色像素(0,0,0),反之
            if ch == '1':
                nd_arr[r][c] = [0, 0, 0]
            elif ch == '0':
                nd_arr[r][c] = [255, 255, 255]
            if c + 1 > 255:
                r = r + 1
                c = 0
            else:
                c = c + 1
    for x in range(r, row):
        for y in range(c, 256):
            nd_arr[x][y] = [255, 255, 255]
    img = Image.fromarray(nd_arr)
    w, d = img.size
    img.save(path)
    print(f'图片尺寸为{w}x{d}，保存成功...')


# 二进制数组转bytes,转utf-8
def bin_to_str(arr):
    res = []
    for i in range(len(arr)):
        res.append(int(arr[i], 2))
    res = bytes(res)
    return res
# .decode('utf-8')


# 图片转ndarray数组,ASCII码转二进制
def image_to_array(img_path):
    img = Image.open(img_path)
    img_arr = np.array(img)
    row = len(img_arr)
    col = len(img_arr[0])
    res_arr = []
    tmp = ''
    count = 1
    for i in range(row):
        for j in range(col):
            if count > 8:
                res_arr.append(tmp)
                count = 1
                tmp = ''
            # 1代表一个黑色像素(0,0,0)
            if img_arr[i][j][0] == 0:
                tmp = tmp + '1'
            # 0代表一个白色像素(255,255,255)
            else:
                tmp = tmp + '0'
            count = count + 1
    return res_arr


def get_time(ext):
    t = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    return f'{t}.{ext}'


# 处理输入
def deal_input():
    info = ""
    save_name = ""
    deal_type = False
    re_confirm = 0
    while True:
        way = input("Bit图片加解密工具【1.解密】[2.加密][0.退出]：")
        if way == '' or way == '1':
            deal_type = True
        elif way == '2':
            deal_type = False
        elif way == '0':
            input('退出程序...')
            break
        # 解密
        if deal_type:
            while True:
                img_path = input('输入密文图片路径：')
                if not img_path == "" and os.path.isfile(img_path):
                    break
                elif img_path.find('http') > -1:
                    res = requests.get(img_path)
                    img_path = get_time('png')
                    with open(img_path, 'wb') as fs:
                        fs.write(res.content)
                        print('成功保存在线图片！')
                    break
            bin_arr = image_to_array(img_path)
            word = bin_to_str(bin_arr)
            while True:
                if re_confirm == 2:
                    re_confirm = 0
                    break
                mod = input(f'解密文字长度为：{len(word)}，选择是否保存为文件[y.保存文件 n.尝试打印utf-8 ]:')
                if mod == 'y' or mod == '':
                    txt_name = input('输入保存的明文文件名[后缀txt](同级目录)[默认：当前时间]:')
                    if txt_name == '':
                        txt_name = get_time('txt')
                    elif txt_name.find('.') < 0:
                        txt_name = txt_name + '.txt'
                    with open(txt_name, 'wb') as tf:
                        tf.write(word)
                    break
                elif mod == 'n':
                    if len(word) > 1000:
                        word_tmp = f'{word[:999]}...等{len(word)-999}个字符'
                        re_confirm = re_confirm + 1
                    else:
                        word_tmp = word
                        re_confirm = 2
                    try:
                        print(word_tmp.decode('utf-8'))
                    except AttributeError:
                        print('尝试解码utf-8失败！')
                        print(word_tmp)
        # 加密
        else:
            while True:
                flag = input('是否加密文件(y/n)：')
                if flag == '' or flag == 'y' or flag == 'Y':
                    flag = True
                    break
                elif flag == 'N' or flag == 'n':
                    flag = False
                    break
            if flag:
                while True:
                    msg_path = input('输入明文信息的文件路径：')
                    if not msg_path == "" and os.path.isfile(msg_path):
                        break
                    elif msg_path.find('http') > -1:
                        res = requests.get(msg_path)
                        msg_path = get_time('png')
                        with open(msg_path, 'wb') as fs:
                            fs.write(res.content)
                            print('成功保存在线图片！')
                        break
                with open(msg_path, 'rb') as file:
                    info = file.read()
            else:
                info = input('输入明文信息(不能换行)：')
            save_name = input('输入保存的密文图片名[后缀png](同级目录)[默认：当前时间]:')
            if save_name == '':
                save_name = get_time('png')
            elif save_name.find('.') < 0:
                save_name = save_name + '.png'
            bin_arr = str_to_bin(info)
            array_to_image(bin_arr, save_name)
        input("操作完成...")
        print('-' * 40)


if __name__ == "__main__":
    deal_input()
