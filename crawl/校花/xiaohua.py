#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 校花


'''
http://www.xiaohuar.com/list-1-0.html 第一页
http://www.xiaohuar.com/list-1-1.html 第二页
'''
import json
import re

import requests
from bs4 import BeautifulSoup

url = 'http://www.xiaohuar.com/list-1-2.html'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def crawl():
    html = requests.get(url=url, headers=header)
    try:
        if html.status_code == 200:
            cont = html.text
            # print(cont)
            soup = BeautifulSoup(cont, 'html.parser')
            items1 = soup.find_all("div", class_='title')
            # 解析 图片地址跟 名字
            urlAndName = re.findall(r'<a href="(.*?)" target="_blank">(.*?)</a></span></div>',
                                    string=str(items1))
            # 解析赞的数目
            items2 = soup.find_all("div", class_='item_b clearfix')
            likeNum_List = re.findall(pattern=r'>(\d+)</em>', string=str(items2))
            resList = []
            resDict = {}
            # 个人喜欢把两个列表放在一起再去转化为字典
            for i in zip(urlAndName, likeNum_List):
                resList.append(list(i))
            for i in range(len(resList) - 1):
                d = {}
                d['url'] = resList[i][0][0]
                d['name'] = resList[i][0][1]
                d['like'] = resList[i][1]
                resDict[i] = d
            return resDict
        else:
            print('web 打不开！请联系：15815773235')
    except Exception as ex:
        print(ex)


def writeJson(self, dic={}):
    with open("./schoolBaby.json", "w", encoding='utf-8') as f:
        json.dump(dic, f)
        print("加载入文件完成...")


if __name__ == '__main__':
    writeJson(crawl())
