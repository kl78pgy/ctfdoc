# coding:utf8
import numpy as np
import cv2
import queue
from pytesseract import *
from PIL import Image
# 自适应阀值二值化
def _get_dynamic_binary_image(img_name):
    # filename =   './out_img/' + img_name.split('.')[0] + '-binary.jpg'
    # img_name = filedir + './' + img_name
    # print('.....' + img_name)
    im = cv2.imread(img_name)
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) #灰值化
    # 二值化
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    # cv2.imwrite(filename,th1)
    cv2.imwrite(img_name,th1)
    return th1

# 去除边框
def clear_border(img,img_name):
    filename = './out_img/' + img_name.split('.')[0] + '-clearBorder.jpg'
    h, w = img.shape[:2]
    for y in range(0, w):
        for x in range(0, h):
            if y < 2 or y > w - 2:
                img[x, y] = 255
            if x < 2 or x > h -2:
                img[x, y] = 255
    cv2.imwrite(filename,img)
    return img

# 干扰线降噪
def interference_line(img, img_name):
    # filename =  './out_img/' + img_name.split('.')[0] + '-interferenceline.jpg'
    h, w = img.shape[:2]
    # ！！！opencv矩阵点是反的
    # img[1,2] 1:图片的高度，2：图片的宽度
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                img[x, y] = 255
    # cv2.imwrite(filename,img)
    cv2.imwrite(img_name,img)
    return img

# 点降噪
def interference_point(img,img_name, x = 0, y = 0):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # filename =  './out_img/' + img_name.split('.')[0] + '-interferencePoint.jpg'
    # todo 判断图片的长宽度下限
    cur_pixel = img[x,y]# 当前像素点的值
    height,width = img.shape[:2]
    for y in range(0, width - 1):
      for x in range(0, height - 1):
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右上顶点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最上非顶点,6邻域
                sum = int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        elif y == width - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右下顶点
                sum = int(cur_pixel) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最下非顶点,6邻域
                sum = int(cur_pixel) \
                      + int(img[x - 1, y]) \
                      + int(img[x + 1, y]) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x + 1, y - 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
            else:  # 具备9领域条件的
                sum = int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 4 * 245:
                  img[x, y] = 0
    # cv2.imwrite(filename,img)
    cv2.imwrite(img_name,img)
    return img
#用队列和集合记录遍历过的像素坐标代替单纯递归以解决cfs访问过深问题
def cfs(im,x_fd,y_fd):
    xaxis=[]
    yaxis=[]
    visited =set()
    q = queue.Queue()
    q.put((x_fd, y_fd))
    visited.add((x_fd, y_fd))
    offsets=[(1, 0), (0, 1), (-1, 0), (0, -1)]#四邻域
    while not q.empty():
        x,y=q.get()
        for xoffset,yoffset in offsets:
            x_neighbor,y_neighbor = x+xoffset,y+yoffset
            if (x_neighbor,y_neighbor) in (visited):
                continue  # 已经访问过了
            visited.add((x_neighbor, y_neighbor))
            try:
                if im[x_neighbor, y_neighbor] == 0:
                    xaxis.append(x_neighbor)
                    yaxis.append(y_neighbor)
                    q.put((x_neighbor,y_neighbor))
            except IndexError:
                pass
  # print(xaxis)
    if (len(xaxis) == 0 | len(yaxis) == 0):
        xmax = x_fd + 1
        xmin = x_fd
        ymax = y_fd + 1
        ymin = y_fd
    else:
        xmax = max(xaxis)
        xmin = min(xaxis)
        ymax = max(yaxis)
        ymin = min(yaxis)
        #ymin,ymax=sort(yaxis)
    return ymax,ymin,xmax,xmin
#搜索区块起点
def detectFgPix(im,xmax):
    h,w = im.shape[:2]
    for y_fd in range(xmax+1,w):
        for x_fd in range(h):
            if im[x_fd,y_fd] == 0:
                return x_fd,y_fd
#'''切割字符位置'''
def CFS(im):
  zoneL=[]#各区块长度L列表
  zoneWB=[]#各区块的X轴[起始，终点]列表
  zoneHB=[]#各区块的Y轴[起始，终点]列表
  xmax=0#上一区块结束黑点横坐标,这里是初始化
  for i in range(10):
    try:
        x_fd,y_fd = detectFgPix(im,xmax)
        # print(y_fd,x_fd)
        xmax,xmin,ymax,ymin=cfs(im,x_fd,y_fd)
        L = xmax - xmin
        H = ymax - ymin
        zoneL.append(L)
        zoneWB.append([xmin,xmax])
        zoneHB.append([ymin,ymax])
    except TypeError:
        return zoneL,zoneWB,zoneHB
  return zoneL,zoneWB,zoneHB

def cutting_img(im,im_position,img,xoffset = 1,yoffset = 1):
    # filename =  './out_img/' + img.split('.')[0]
      # 识别出的字符个数
    im_number = len(im_position[1])
    # 切割字符
    for i in range(im_number):
        im_start_X = im_position[1][i][0] - xoffset
        im_end_X = im_position[1][i][1] + xoffset
        im_start_Y = im_position[2][i][0] - yoffset
        im_end_Y = im_position[2][i][1] + yoffset
        cropped = im[im_start_Y:im_end_Y, im_start_X:im_end_X]
        # cv2.imwrite(filename + '-cutting-' + str(i) + '.jpg',cropped)
        cv2.imwrite(img + '-cutting-' + str(i) + '.jpg',cropped)
def vode_str(img_name):
    # 识别验证码
    img=_get_dynamic_binary_image(img_name)
    img=interference_line(img,img_name)
    img=interference_point(img,img_name)
    xyfd=detectFgPix(img,4)
    pics=cfs(img,xyfd[0],xyfd[1])
    im_position=CFS(img)
    cutting_img(img,im_position,img_name,1,1)
    try:
        # file = './out_img/%s-cutting-%s.jpg' % (img_name.split('.')[0], i)
        # 识别字符
        # str_img = str_img + image_to_string(Image.open(file),lang = 'eng', config='-psm 10') #单个字符是10，一行文本是7
        str_img=image_to_string(img)
    except Exception as err:
        pass
    # print('切图：%s' % cutting_img_num)
    print('识别为：%s' % str_img)

vode_str('E:\\codeworker\\CTF\\360img\\code0.jpg')