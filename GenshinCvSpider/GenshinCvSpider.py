

import asyncio
import json
import os.path
import time
import random

from pyppeteer import launch
from lxml import etree
import re

# url = 'https://bbs.mihoyo.com/ys/obc/content/3875/detail'
# role = '神里绫人'
browser = None
url_arr = []
role_arr = []
reg = re.compile(r'(<body>[\s\S]+</body>)')
xpath = "//div[@data-part='voiceTab']/ul[2]/li[1]/table[2]/tbody/tr"
config = {
    'headless': True,
    'dumpio': True,
    'autoClose': False,
    'userDataDir': r'D:\temporary',
    'args': [
        '--no-sandbox',
        '--window-size=1920,5000',
        '--disable-infobars'
    ]
}


# 解码：将二进制字符串转换为原来的字符串
def uni_decode(s):
    return etree.tounicode(s)


# xpath选取节点
def get_xpath(el, xp="text()"):
    res = el.xpath(xp)
    if len(res) > 0:
        return res[0]
    else:
        return ''


# 获取语录
def get_word(word):
    if word == '':
        return ''
    word = word.replace(' ', '')
    word = word.replace('\n', '')
    return word


# 获取随机等待时间
def rand_time():
    return random.randint(200, 600) / 100


# 开始上网爬虫
async def start_web(role, url):
    global browser
    global reg

    html = etree.HTML('')
    word_list = []
    page_text = ''

    # 跳转网页
    try:
        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 5000})
        # js为设置webdriver的值，防止网站检测
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        await page.goto(url)
        time.sleep(2)
        page_text = await page.content()  # 获取网页源码
        await page.close()
    except Exception as e:
        page_text = ''
        print('跳转网页: err！', e)

    try:
        m = reg.findall(page_text)
        if m and len(m) > 0:
            html = etree.HTML(m[0])
        elements = html.xpath(xpath)
        for i, els in enumerate(elements):
            # 处理中文并构造HTML
            els = etree.HTML(uni_decode(els))
            # xpath匹配元素
            word_title = get_xpath(els, "//td[@class='h3']")
            word_content = get_xpath(els, "//span[@class='obc-tmpl-character__voice-content']")
            cv_url = get_xpath(els, "//source/@src")
            # 获取匹配元素的文本
            word_title = get_word(get_xpath(word_title))
            word_content = get_word(get_xpath(word_content))
            word_list.append({
                "id": i + 1,
                "name": role,
                "title": word_title,
                "content": word_content,
                "cv": cv_url
            })
        print('{0} success!'.format(role))
    except Exception as e:
        print('{0} 获取元素: fail! {1}'.format(role, e))

    write_txt(role, word_list)


# 写入json文件
def write_txt(role_name, data):
    path = './RoleCV/{0}.json'.format(role_name)
    # utf-8编码写入
    with open(path, 'w', encoding='utf-8') as f:
        # 写入json，处理中文
        json.dump({"RECORDS": data}, f, indent=4, ensure_ascii=False)
        # f.write(json.dumps({"RECORDS": obj}, indent=4, ensure_ascii=False))


# 初始化角色名和链接
def init_data():
    global url_arr
    global role_arr
    with open('mhyRoleUrl.txt', 'r') as f:
        url_arr = [x.replace('\n', '') for x in f.readlines()]
        f.close()
    with open('mhyRoleName.txt', 'r', encoding='utf-8') as f:
        role_arr = [x.replace('\n', '') for x in f.readlines()]
        f.close()


# 开始循环爬虫
async def start_spider():
    global url_arr
    global role_arr
    global browser
    browser = await launch(config)
    print('browser launched!')
    await browser.newPage()
    for (r, u) in zip(role_arr, url_arr):
        r_time = rand_time()
        if os.path.exists('./RoleCV/{0}.json'.format(r)):
            print('{0} {1} start... {2}s'.format(r, u, r_time + 2))
            await start_web(r, u)
            time.sleep(r_time)
        else:
            print('{0} skip.'.format(r))
    await browser.close()
    print('browser closed!')


def edit_data():
    dir_path = os.listdir('./RoleCV')
    for file in dir_path:
        file_path = './RoleCV/{0}'.format(file)
        name = file.split('.')[0]
        print('修改 {0}'.format(file))
        with open(file_path, encoding='utf-8') as f:
            data = json.loads(f.read().encode('utf-8'))
            records = data.get('RECORDS')
            print(records)
            for i, item in enumerate(records):
                # 自定义字段
                records[i]['name'] = name
            f.close()
        write_txt(name, records)
        print('{0} ok!'.format(name))


if __name__ == '__main__':
    # 爬虫
    init_data()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(start_spider()))
    # 修改数据
    # edit_data()
