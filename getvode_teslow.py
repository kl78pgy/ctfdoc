#!/usr/bin/env python
# coding=UTF-8

import re
import time
import hashlib
import base64
import json
import requests
from captcha_trainer.predict_testing import predict_img

# 代理设置
proxy = 'http://127.0.0.1:8080'
use_proxy = False  

MY_PROXY = None
if use_proxy:
    MY_PROXY = {
        # 本地代理，用于测试，如果不需要代理可以注释掉
        'http': proxy,
        'https': proxy,
    }
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,ja;q=0.9,zh-HK;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
}

def md5(data):
    md5 = hashlib.md5(data.encode('utf-8'))
    return md5.hexdigest()

def http_req(url, data=None, method='GET', params=None, json=False, cookies=None, proxies=MY_PROXY):
    if json:
        method = 'POST'
        json = data
        data = None
    if method == 'GET':
        params = data
        data = None
    r = requests.request(method, url, headers=headers, verify=False, json=json,
                         params=params, data=data, cookies=cookies, proxies=MY_PROXY)
    return r

def calc_req(url, data=None):
    global my_cookie
    result = http_req(url, data=data, cookies=my_cookie)
    my_cookie = result.cookies
    return result

calc_url = "http://127.0.0.1:8800/"
calc_pic = calc_url + "imgcode"
calc_check = calc_url + "checkexp"

def print_round(txt):
    round_txt = re.search("round.*", txt)
    if round_txt:
        print(round_txt[0])

my_cookie = {
}
r = calc_req(calc_url)
print_round(r.text)
# 由于10次图片识别不一定每次都正确，采用循环直到发现flag
while True:
    pic = calc_req(calc_pic)
    exp = predict_img('360-CNNX-GRU-H64-CTC-C1','E:/codeworker/CTF/360img','code1717.jpg')
    result = eval(exp)
    time.sleep(0.3)
    r2 = calc_req(calc_check, {'result': result})
    print_round(r2.text)
    if len(r2.history) == 0:  # 没有302重定向，则输出结果cls
        print(r2.text)
        break