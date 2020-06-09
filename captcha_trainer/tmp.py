# -*- coding: utf-8 -*-
# @Time :2018/8/25   20:18
# @Author : ELEVEN
# @File : 011_批量重命名文件.py
# @Software: PyCharm
import os
import matplotlib.pyplot as plt
from PIL import Image
import time
import psutil
# 1. 获取一个要重命名的文件夹的名字
folder_name = 'E:\\codeworker\\CTF\\360img\\'

# 2. 获取那个文件夹中所有的文件名字
file_names = os.listdir(folder_name)

# 第1中方法
# os.chdir(folder_name)

# 3. 对获取的名字进行重命名即可
# for name in file_names:
#    print(name)
#    os.rename(name,"[京东出品]-"+name)
i = 1 # 可以让每个文件名字都不一样

for name in file_names:
    print(name)
    print(name.split('.')[-1])
    name1 = name.split('.')[0]
    name2=name.split('.')[-1]
    old_file_name = folder_name +  name
    # fp = open(old_file_name,'rb')
    # img = Image.open(fp)
    # #这里改为文件句柄
    # img.show()
    # time.sleep(3)
    # fp.close()
    image = Image.open(old_file_name)
    
    plt.figure(figsize=(4, 4))
    # plt.ion()  # 打开交互模式
    plt.axis('off')  # 不需要坐标轴
    plt.imshow(image) 
    mngr = plt.get_current_fig_manager()
    mngr.window.wm_geometry("+1380+310")  # 调整窗口在屏幕上弹出的位置
    plt.pause(1)  # 该句显示图片15秒   
    # plt.ioff()  # 显示完后一定要配合使用plt.ioff()关闭交互模式，否则可能出奇怪的问题
    # plt.clf()  # 清空图片
    # process_list = []
    # for proc in psutil.process_iter():
    #     process_list.append(proc)
    # image.show()
    # for proc in psutil.process_iter():
    #     if not proc in process_list:
    #         proc.kill()
        
    new_name=input("请输入要重命名的:")     
    plt.close()
    new_file_name = folder_name+  new_name +"_"+str(i) +'.'+name2
    os.rename(old_file_name, new_file_name)
    i += 1