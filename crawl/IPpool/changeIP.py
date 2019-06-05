#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   :

import requests
import re
''' 
    

'''
class Revenge(object):
    def __init__(self):
        pass

import requests
header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
try:
    requests.get('http://baidu.com/',headers=header, proxies={"http": "163.204.244.127:9999"})
except Exception as ex:
    print(ex)
    print('connect failed')
else:
    print('success')