# -*- coding:utf-8 -*-
import os
import re
import time
import requests
# pyinstaller -F ImageDownload.py -i down.ico --hidden-import=requests


# 读取文件的第一行控制字符串
CONFIG = [
    '[start]',
    '[end]'
]
contain_arr = []
filter_arr = []
download_count = 0


# 替换保存文件名的特殊字符
def rename(name):
    name_re = re.compile("[\\/:*?\"<>|]")
    return name_re.sub('_', name)


# 按行读取文件，返回一个数组
def read_line(file):
    arr = []
    try:
        file = open(file, 'r', encoding='utf-8')
        while True:
            line = file.readline()
            if line:
                line_str = line.replace('\n', '')
                if line_str:
                    arr.append(line_str)
            else:
                break
        file.close()
    except FileNotFoundError:
        print('文件读取失败！')
        pass
    return deal_arr(arr)


# 拼接数组的每一项
def deal_arr(arr):
    al = len(arr)
    if al == 0:
        return []
    res = []
    if arr[0].find(CONFIG[0]) > -1:
        tmp = arr[0].replace(CONFIG[0], '')
        for i in range(1, al):
            res.append(f'{tmp}{arr[i]}')
    elif arr[0].find(CONFIG[1]) > -1:
        tmp = arr[0].replace(CONFIG[1], '')
        for i in range(1, al):
            res.append(f'{arr[i]}{tmp}')
    else:
        return arr
    return res


# 下载图片
def download_image(url, outfile, file):
    global download_count
    try:
        if os.path.isfile(outfile):
            print(f'{file} 已存在')
            return
        else:
            print(f'{file} 下载中...')
        pic = requests.get(url)
        fp = open(outfile, 'wb')
        fp.write(pic.content)
        download_count = download_count + 1
        fp.close()
    except requests.exceptions.ConnectionError:
        print(f'{url}，下载失败！')


# 包含和过滤,判断名称是否满足
def check(name):
    global contain_arr
    global filter_arr
    lc = len(contain_arr)
    lf = len(filter_arr)
    # 包含是否满足，过滤是否满足
    flag = [False, True]
    # 判断包含条件，满足就为真，保留。不满足为假，舍弃。
    if lc > 0:
        for i in range(lc):
            if name.find(contain_arr[i]) > -1:
                flag[0] = True
                break
    else:
        flag[0] = True
    # 判断过滤条件，满足就为假，舍弃。不满足为真，保留。
    if lf > 0:
        for i in range(lf):
            if name.find(filter_arr[i]) > -1:
                flag[1] = False
                break
    if flag[0] and flag[1]:
        return True
    return False


# 开始批量下载
def start_download(urls, names, out_name, ext):
    if not os.path.isdir(out_name):
        os.mkdir(out_name)
    if ext == "" or ext == "auto":
        ext = 'png'
    for url, name in zip(urls, names):
        real_name = rename(name)
        if not check(name):
            print(f'{real_name} 已过滤！')
            continue
        out_path = f'{out_name}/{real_name}.{ext}'
        download_image(url, out_path, f'{real_name}.{ext}')


def get_time():
    t = time.gmtime()
    return time.strftime("%Y-%m-%d %H-%M-%S", t)


# 处理输入
def deal_input():
    global url_path, name_path, out_dir, ext_name, contain_arr, filter_arr
    while True:
        url_path = input('输入链接的TXT文件路径：')
        if os.path.isfile(url_path):
            url_path = url_path.replace('\"', '')
            break
    while True:
        name_path = input('输入文件名的TXT文件路径：')
        if os.path.isfile(name_path):
            name_path = name_path.replace('\"', '')
            break
    while True:
        out_dir = input('输入保存的文件夹名[默认：images+当前时间]：')
        if out_dir == "":
            out_dir = f'images {get_time()}'
            break
        if not os.path.isdir(out_dir):
            break
    while True:
        ext_name = input('输入保存图片的后缀名[默认：png]：')
        if ext_name == "":
            ext_name = 'png'
            break
    while True:
        contain_arr_str = input('输入必须包含的字符(空格分割)[默认：无]：')
        tmp = contain_arr_str.split(' ')
        tmp = map(lambda x: not x == "", tmp)
        if contain_arr_str == "":
            contain_arr = []
            break
        elif len(tmp) > 0:
            contain_arr = tmp
            break
    while True:
        filter_arr_str = input('输入需要过滤的字符(空格分割)[默认：无]：')
        tmp = filter_arr_str.split(' ')
        tmp = map(lambda x: not x == "", tmp)
        if contain_arr_str == "":
            filter_arr = []
            break
        elif len(tmp) > 0:
            filter_arr = tmp
            break
    return url_path, name_path, out_dir, ext_name, contain_arr, filter_arr


if __name__ == '__main__':
    url_path, name_path, out_dir, ext_name, contain_arr, filter_arr = deal_input()
    url_arr = read_line(url_path)
    name_arr = read_line(name_path)
    print('-'*20)
    print(f'链接和名称TXT文件的记录数量：{len(url_arr)},{len(name_arr)}')
    print(f'包含字段：{contain_arr}\n过滤字段：{filter_arr}\n')
    start_download(url_arr, name_arr, out_dir, ext_name)
    print('-' * 20)
    input(f'\n共{download_count}张图片，下载完成...')
