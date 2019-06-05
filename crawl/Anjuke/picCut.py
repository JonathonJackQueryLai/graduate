#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   :
# import time
# from selenium import webdriver
#
# driver = webdriver.Firefox()
# driver.implicitly_wait(6)
# driver.get("https://www.baidu.com")
# time.sleep(1)
#
# driver.get_screenshot_as_file("F:\\baidu.png")
# driver.quit()


from PIL import Image
def funcCut():
    im = Image.open("huitu.png")
    # 图片的宽度和高度
    img_size = im.size
    # print("图片宽度和高度分别是{}".format(img_size))
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    '''
    # 截取图片中一块宽和高都是250的
    x = 720
    y = 337
    w = 114
    h = 51
    # region = im.crop((x, y, w, h))
    region = im.crop((x, y, x+w, y+h))
    # x = 100
    # y = 100
    # w = 250
    # h = 250
    # region = im.crop((x, y, x+w, y+h))
    region.save("res.png")

# # 截取图片中一块宽是250和高都是300的
# x = 100
# y = 100
# w = 250
# h = 300
# region = im.crop((x, y, x+w, y+h))
# region.save("./crop_test2.jpeg")
