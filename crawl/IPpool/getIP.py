#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   :

import re

import pymongo
# import lxml
import requests


class IPSpider(object):
    def __init__(self):
        self.__name = '获取IP'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
        self.resultList = []
        self.start_url = 'https://www.kuaidaili.com/free/inha/'

    def run(self):
        for num in range(1, 10):
            url = self.start_url + str(num) + '/'
            html = requests.get(self.start_url,proxies='{"http":"http://121.31.154.12:8123"}')
            try:
                if html.status_code == 200:
                    print(url)
                    content = html.text
                    IP = re.findall(r'<td data-title="IP">(.*?)</td>', content)
                    port = re.findall(r'<td data-title="PORT">(.*?)</td>', content)
                    no_name = re.findall(r'<td data-title="匿名度">(.*?)</td>', content)
                    type = re.findall(r'<td data-title="类型">(.*?)</td>', content)
                    site = re.findall(r'<td data-title="位置">(.*?)</td>', content)
                    responeSpeed = re.findall(r'<td data-title="响应速度">(.*?)</td>', content)
                    lastTime = re.findall(r'<td data-title="最后验证时间">(.*?)</td>', content)
                    # print(IP)
                    # print(port)
                    # print(no_name)
                    # print(type)
                    # print(site)
                    # print(responeSpeed)
                    # print(lastTime)
                    for i in zip(IP, port, no_name, type, site, responeSpeed, lastTime):
                        self.resultList.append(i)
                    # break
            except Exception as ex:
                print('somthing happend %s' % ex)

        else:
            print("html解析失败！")
        return self.resultList

    def dictFormat(self, demoList=[]):
        IPDict = {}
        IPList = []
        for i in range(len(demoList)):
            demoList[i] = [str(i)] + list(demoList[i])
        for i in demoList:
            IPDict[str(i[0])] = i[1::]
        # print(IPDict)
        return IPDict


class MonDb(object):
    def __init__(self, db_name, col_name):
        self.conn = pymongo.MongoClient('127.0.0.1', 27017)
        self.db_name = self.conn[db_name]
        self.col_name = self.db_name[col_name]

    def insert(self, data):
        if isinstance(data, list):
            self.col_name.insert_many(data)
        elif isinstance(data, dict):
            self.col_name.insert_one(data)

    def delete(self, query, _all=False):
        if _all:
            self.col_name.delete_many(query)
        else:
            self.col_name.delete_one(query)

    def update(self, query, data):
        self.col_name.update_many(query, data)

    def find(self, query, _all=False):
        if _all:
            return self.col_name.find(query)
        else:
            return self.col_name.find_one(query)


if __name__ == '__main__':
    myIP = IPSpider()
    MyM = MonDb('IP', 'store')
    resDict = myIP.dictFormat(myIP.run())
    # print(resDict)
    MyM.insert(resDict)
