#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   :
import time

import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from PIL import ImageFont, Image, ImageDraw
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# from .chaojiying import GanJiVcCdeo
from crawl.Anjuke.chaojiying import chaojiying_Run

class VCode(object):
    def __init__(self):
        self.__name = '二手房爬虫'

        self.driver = webdriver.Firefox()

        self.start_url = 'https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam&serialID=9fd34110c7a80f9cf57058c2836bd820_1a5323c46e7b4642a2ee97388ec87da8&history=aHR0cHM6Ly93d3cuYW5qdWtlLmNvbS8%3D'

    # 一直等待某元素可见，默认超时10秒
    def is_visible(self, locator, timeout=10):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    # 一直等待某个元素消失，默认超时10秒
    def is_not_visible(self, locator, timeout=10):
        try:
            ui.WebDriverWait(self.driver, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def funcCut(self,picName):
        im = Image.open(picName)
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
        region = im.crop((x, y, x + w, y + h))

        # x = 100
        # y = 100
        # w = 250
        # h = 250
        # region = im.crop((x, y, x+w, y+h))
        region.save("screen1.png")
    # 添加字体
    def addFont(self,picName):
        # 设置字体，如果没有，也可以不设置
        font = ImageFont.truetype("STSONG.ttf", size=25)  # Baidu and download file 华文细黑.ttf

        # 打开底版图片
        # imageFile = 'screen.png'  # 白色的图片
        im1 = Image.open(picName)

        # 在图片上添加文字 1
        draw = ImageDraw.Draw(im1)
        draw.text((1, 1), "按顺序返回两个小方块的中点", fill='red', font=font)

        # 保存
        im1.save("yidong.png")
    # 获取 距离 221,103|29,96
    def get_track(self,distanceStr = ''.strip(''),typeName=''):
        # 第一道防线
        if typeName == '1':
            Dlist = distanceStr.split('|')
            x1 = int(Dlist[0][0])
            x2 = int(Dlist[0][1])
            distance = int(abs(x1-x2))+1
            return distance

        elif typeName == '2':
            # 第二道防线
            pass

    def run1(self):
        self.driver.get(url=self.start_url)
        # //
        # // *[ @ id = "ISDCaptcha"] / div[2] / div[3]
        # MoveSlider = self.driver.find_element_by_xpath('*[@id="ISDCaptcha"]/div[2]/div[3]')
        # 等待验证码的加载
        time.sleep(2)
        flashPic = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/form/div/div[1]/div/div/div')
        time.sleep(1)
        flashPic.click()
        html = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        print('源码：',html)
        time.sleep(3)
        MoveSlider = self.driver.find_element_by_xpath('//*[@id="ISDCaptcha"]/div[2]/div[3]/svg')
        print('第一步,点击滑动按钮')
        MoveSlider.click()
        time.sleep(1)
        if self.is_not_visible('//*[@id="dvc-captcha__canvas"]'):
            img = self.driver.find_element_by_xpath('//*[@id="dvc-captcha__canvas"]')
        else:
            print('还没出现有问题')
        self.driver.get_screenshot_as_png("screen.png")
        self.funcCut('screen.png')
        self.addFont('screen1.png')

        startTime = time.time()
        # 坐标
        coordinate = chaojiying_Run(('安居客'))
        time.sleep(1)
        print('消耗的时间为：', time.time() - startTime)
        ActionChains(self.driver).click_and_hold(on_element=MoveSlider).perform()  # 点击鼠标左键，按住不放
        print('第二步,拖动元素')
        track = self.get_track(coordinate)
        ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）

        time.sleep(0.5)
        print('第三步,释放鼠标')
        ActionChains(self.driver).release(on_element=MoveSlider).perform()
        # self.driver.quit()


if __name__ == '__main__':
    myC = VCode()
    myC.run1()
