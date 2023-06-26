#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__ = "Michael Yu"
# Filename: downloadPic.py
# Date: 2023/6/25

import os
import time
import requests
import hashlib
from operator import itemgetter

# 常量
SALT = 'laxiaoheiwu'
COUNT = 9999

# 定义请求的参数
data = {
    'activityNo': 0,
    'isNew': False,
    'count': COUNT,
    'page': 1,
    'ppSign': 'live',
    'picUpIndex': '',
    '_t': 0,
}

# 对象按键排序
def obj_key_sort(obj):
    sorted_obj = sorted(obj.items(), key=itemgetter(0))
    sorted_obj_dict = {k: str(v) for k, v in sorted_obj if v is not None}
    return '&'.join([f"{k}={v}" for k, v in sorted_obj_dict.items()])

# MD5加密
def md5(value):
    m = hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()

# 获取所有图片
def get_all_images(id,place):
    image_path = "../Pics/" + str(place)
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    t = int(time.time() * 1000)
    data['activityNo'] = id
    data['_t'] = t
    data_sort = obj_key_sort(data)
    sign = md5(data_sort + SALT)
    params = {
        **data,
        '_s': sign,
        'ppSign': 'live',
        'picUpIndex': '',
    }
    try:
        res = requests.get('https://live.photoplus.cn/pic/pics', params=params)
        res.raise_for_status()  # 如果响应状态不是200，就主动抛出异常
    except requests.RequestException as err:
        print("Oops: Something Else Happened",err)
        return
    try:
        res_json = res.json()
    except ValueError:
        print("Response content is not valid JSON")
        return

    total_pics = res_json['result']['pics_total']
    camer = res_json['result']['pics_array'][0]['camer']

    i = total_pics + 1
    j = 0
    for pic in res_json['result']['pics_array']:
        image_name = pic['pic_name']
        download_all_images(("https:" + pic['origin_img']),image_path,image_name)
        i = i - 1
        j = j + 1
        print("正在下栽第{}张 - 文件名:{}".format(i,image_name))
    print("Total Photos:{} - Downloaded:{} - Photographer:{}".format(total_pics,j,camer))

# 下载图片
def download_all_images(url,image_path,image_name):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果响应状态不是200，就主动抛出异常
    except requests.RequestException as err:
        print("Oops: Something Else Happened",err)
        return
    time.sleep(2)
    with open(os.path.join(image_path, image_name), 'wb') as out_file:
        out_file.write(response.content)

id = input("Enter photoplus ID (eg:87654321): ")
count = input("Enter number of photos (Default:9999): ")
place = input("Enter where will you go: ")

if count.isnumeric():
  data['count'] = int(count)
if id.isnumeric():
  get_all_images(int(id),place)
else:
  print('Wrong ID')
