#!/usr/bin/env python
# coding:utf-8
import hashlib
import math
import time

import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

"""
    MD5: C734C4372BB422EDCA8F3E32D0D321CA
    SHA1: 3EC2079B9B5CCAC3B51A9F955110F095A2AD7EB1
    CRC32: 1166E524
"""


# 发送代码的
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = hashlib.md5(password.encode("UTF-8")).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


# 添加字体
def addFont():
    # 设置字体，如果没有，也可以不设置
    font = ImageFont.truetype("STSONG.ttf", size=25)  # Baidu and download file 华文细黑.ttf

    # 打开底版图片
    imageFile = 'yidong.png'  # 白色的图片
    im1 = Image.open(imageFile)

    # 在图片上添加文字 1
    draw = ImageDraw.Draw(im1)
    draw.text((1, 1), "返回两个小方块的中点", fill='red', font=font)

    # 保存
    im1.save("yidong.png")


#  计算轨迹
class GanJiTrack(object):

    def p2p(self, string=''):

        # map
        def format(x):
            return int(x)

        st = '208,138|47,99|144,139|168,71'
        trackList = []
        li = list(st.split('|'))
        li1 = []
        li2 = []
        for numSet in li:
            li1.append(numSet.split(','))

        try:
            for i in li1:
                li2.append(list(map(format, i)))
            for x in range(len(li2) - 1):
                tack = math.sqrt((li2[x + 1][0] - li2[x][0]) ** 2 + (li2[x + 1][1] - li2[x][1]) ** 2)
                trackList.append(int(tack))
        except Exception as ex:
            print('计算出错')

        return trackList


# 计算轨迹
class AnjukeTrack(object):

    # 计算轨迹
    def p2p(self, string=''):
        # map
        def format(x):
            return int(x)

        st = '208,138|47,99|144,139|168,71'
        trackList = []
        li = list(st.split('|'))
        li1 = []
        li2 = []
        for numSet in li:
            li1.append(numSet.split(','))

        try:
            for i in li1:
                li2.append(list(map(format, i)))
            for x in range(len(li2) - 1):
                tack = math.sqrt((li2[x + 1][0] - li2[x][0]) ** 2 + (li2[x + 1][1] - li2[x][1]) ** 2)
                trackList.append(int(tack))
        except Exception as ex:
            print('计算出错')

        return trackList


#
def chaojiying_Run(name=''):
    '''

    9101 	坐标选一,返回格式:x,y 	15
    9102 	点击两个相同的字,返回:x1,y1|x2,y2 	22
    9202 	点击两个相同的动物或物品,返回:x1,y1|x2,y2 	40
    9103 	坐标多选,返回3个坐标,如:x1,y1|x2,y2|x3,y3 	20
    9004 	坐标多选,返回1~4个坐标,如:x1,y1|x2,y2|x3,y3 	25
    9104 	坐标选四,返回格式:x1,y1|x2,y2|x3,y3|x4,y4 	30
    9201 	坐标多选,返回1~5个坐标值 	50

    :param name:  超级鹰返回坐标格式
    :return:
    '''
    cy = Chaojiying_Client('fzj1025', '999jiajiajia999.', '96001')
    im = open('yidong.png', 'rb').read()
    if name == '赶集网' or name == '安居客2':
        # 赶集网
        pic_str = cy.PostPic(im, 9104)
    elif name == '安居客':
        pic_str = cy.PostPic(im, 9202)

    return pic_str["pic_str"]


# start = time.time()
# print(chaojiying_Run('安居客'))
# print('消耗的时间为：',time.time()-start)
