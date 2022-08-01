# -*- coding:utf-8 -*-
import math
import os
# import re
import time

# pyinstaller -F Rename.py -i rename.ico
# --hidden-import=

config = {}


# 读取目录文件列表
def read_dir(path):
    if not os.path.isdir(path):
        print('文件夹路径无效！')
        return
    for root, dirs, files in os.walk(path):
        print(root, dirs, files, '?')
        return files


# 读取文件内容
def read_file(path):
    if not os.path.isfile(path):
        print('文件夹路径无效！')
        return ""
    with open(path, 'r', encoding='UTF-8') as file:
        data = file.read()
        return data


# 生成配置信息
def get_config(txt):
    arr = txt.split('\n')
    dl = len(arr)
    if dl < 5:
        for i in range(5 - dl):
            arr.append('')
    obj = {
        'dir_path': arr[0],
        'option': arr[1],
        'data': arr[2],
        'copy': arr[3],
        'origin': arr[4]
    }
    return obj


# 检查路径
def check_path(path):
    return os.path.isdir(path)


# 处理参数
def deal_config():
    global config
    if not check_path(config['dir_path']):
        print('重命名的目录不存在！')
        return
    old_arr = read_dir(config['dir_path'])
    new_arr = get_new_name(old_arr)
    copy_arr = config['copy'].split(' ')
    if len(copy_arr) == 1:
        path = config['dir_path']
    else:
        path = copy_arr[1].replace('/', "\\")
    if path[-1] == '\\':
        path = path[:-1]
    old_path_arr = list(map(lambda x: f'{path}\\{x}', old_arr))
    new_path_arr = list(map(lambda x: f'{path}\\{x}', new_arr))
    print(old_path_arr, new_path_arr)
    rename(old_path_arr, new_path_arr)
    input(f'原本{len(old_path_arr)}个文件，重命名{len(new_path_arr)}个文件，重命名完成！')


# 不足补充特定字符
def str_fill(org, lg, char):
    n = math.ceil((lg - len(org)) / len(char))
    res = char * n + org
    return res


# 把空字符串/时间类型/时间戳(秒)转日期格式化本地时间
def format_datetime(time_item=None, format_key="%Y-%m-%d-%H-%M-%S"):
    sec = 0
    if type(time_item) == time.struct_time:
        sec = int(time.mktime(time_item))
    elif time_item == "" or not time_item:
        sec = int(time.mktime(time.localtime()))
    elif type(time_item) == str or type(time_item) == float:
        sec = int(time_item)
    return time.strftime(format_key, time.localtime(sec))


# dirPath        <D:\xxxx.txt>                  重命名的文件夹路径
# option         [number,datetime,size,start,end,mid]              重命名方式
# data           number:[,1 1 1 3 x,1,5...]   //(开始数，步长，增减顺序， 不足几位，不足前补充x字符)
#                datetime:[0 %Y-%m-%d-%H-%M-%S, 1 10...]  // 日期时间格式化的参数(日期字符串/时间戳， 格式/保留位数(3-13))
#                size:[,KB,MB 1...]   // （单位，显示单位）
#                end:[xxxx],    // 后缀字符串
#                start:[xxxx],  // 前缀字符串
#                mid:[xxxx,xxxx 5...] // 中间字符串（插入字符串，第几个字符后）           重命名方式的参数
# copy           [0,1 D:\xxxx]                          是否另存为
# origin         [0,1]                          是否保留原名


# 不同方法获取新名称
def get_new_name(old_arr):
    global config
    new_arr = []
    way = config['option']
    data = config['data'].split(' ')
    print(way, data)
    old_len = len(old_arr)
    if way == 'number':
        dl = len(data)
        start = 1 if dl < 1 or (dl == 1 and data[0] == '') else int(data[0])
        step = 1 if dl < 2 else int(data[1])
        order = 1 if dl < 3 else int(data[2])
        length = 0 if dl < 4 else int(data[3])
        char = '0' if dl < 5 else data[4]
        for i in range(old_len):
            name_num = start + order * step * i
            name = str_fill(str(name_num), length, char)
            ext = old_arr[i].split('.')[-1]
            new_arr.append(f'{name}.{ext}')
    elif way == 'datetime':
        method = int(data[0])
        format_way = " ".join(data[1:])
        print(format_way, '?')
        for i in range(old_len):
            c_time = os.stat(f"{config['dir_path']}\\{old_arr[i]}").st_ctime
            if method == 0:
                name = format_datetime(c_time, format_way)
            else:
                m = 10 ** int(format_way)
                name = int(c_time) % m
            ext = old_arr[i].split('.')[-1]
            new_arr.append(f'{name}.{ext}')
    elif way == 'size':
        pass
    return new_arr


# 重命名
def rename(old_arr, new_arr):
    for (old, new) in zip(old_arr, new_arr):
        try:
            os.rename(old, new)
            print(f'{old}重命名成功...')
        except FileExistsError:
            new_info = new.split('\\')
            file_info = new_info[-1].split('.')
            new_path = '\\'.join(new_info[:-1])
            new_tmp = f"{new_path}\\{file_info[0]}-fail.{file_info[1]}"
            try:
                os.rename(old, new_tmp)
                print(f'{old}重命名失败, 命名为{new_tmp}！')
            except FileExistsError:
                print(f'{old}尝试两次重命名失败！！')
        time.sleep(0.2)


# WindowsError: 重命名失败
if __name__ == "__main__":
    txt = read_file('config.txt')
    if txt == "":
        input('未找到config.txt配置文件！')
    else:
        config = get_config(txt)
        print(config)
        deal_config()


