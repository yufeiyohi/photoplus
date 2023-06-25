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
from PIL import Image
from io import BytesIO

SALT = 'laxiaoheiwu'
COUNT = 9999

data = {
    'activityNo': 0,
    'isNew': False,
    'count': COUNT,
    'page': 1,
    'ppSign': 'live',
    'picUpIndex': '',
    '_t': 0,
}

def obj_key_sort(obj):
    sorted_obj = sorted(obj.items(), key=itemgetter(0))
    sorted_obj_dict = {k: str(v) for k, v in sorted_obj if v is not None}
    return '&'.join([f"{k}={v}" for k, v in sorted_obj_dict.items()])

def md5(value):
    m = hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()

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

    res = requests.get('https://live.photoplus.cn/pic/pics', params=params)
    res_json = res.json()
    i = 0
    origin_img_list = []
    print(f"Total Photos: {res_json['result']['pics_total']})
    for pic in res_json['result']['pics_array']:
        download_all_images(("https:" + pic['origin_img']),image_path)
        i = i + 1

    print(f"Total Photos: {res_json['result']['pics_total']}, Downloaded: " + str(i))

def download_all_images(url,image_path):
    image_name = url.split('/')[-1].split('?')[0]
    print(image_name)
    response = requests.get(url)
    time.sleep(2)
    # 确保请求成功
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        # 在你希望的位置保存图片
        img.save(os.path.join(image_path, image_name))

id = input("Enter photoplus ID (eg: 87654321): ")
# count = input("Enter number of photos: ")
place = input("Enter where will you go: ")

# if count.isnumeric():
#   data['count'] = int(count)
if id.isnumeric():
  get_all_images(int(id),place)
else:
  print('Wrong ID')

