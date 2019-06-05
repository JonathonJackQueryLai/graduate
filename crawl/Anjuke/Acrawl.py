#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 安居客
import csv
import re

import pandas as pd
import requests
# funRun()
from bs4 import BeautifulSoup


# 有反爬虫情况


class ArawlSpider(object):
    def __init__(self):
        self.__name = '二手房爬虫'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
        self.resultList = []
        self.start_url = 'https://jiangmen.anjuke.com/sale/'

    # 数据更新
    def datafiller(self, oldUrlList):
        # 只要获取获取第一个页面就行
        targetUrl = self.start_url + 'p1/#filtersort'
        html = requests.get(url=targetUrl, headers=self.header)
        content = html.text
        content1 = content
        urlList = re.findall(
            r'href="(https://jiangmen.anjuke.com/prop/view/A\d+\?from=filter&spread=commsearch_p&position=\d+&kwtype=filter&now_time=\d+)"',
            content)

        difference_url_list = list(set(urlList).difference(set(oldUrlList)))  # 通过找出差集找出新的有的url ,旧的没有
        # 存储起来
        df = pd.read_csv('oldUrlList.csv')
        df['list'] = difference_url_list
        df.to_csv('oldUrlList.csv', index=None)
        return difference_url_list

    def dataCrawl(self):
        for i in range(1, 51):
            rangeUrl = self.start_url + 'p{0}/#filtersort'.format(i)
            print(rangeUrl)
            html = requests.get(url=rangeUrl, headers=self.header)
            content = html.text
            content1 = content

            # soup = BeautifulSoup(content1, "html.parser")
            urlList = re.findall(
                r'href="(https://jiangmen.anjuke.com/prop/view/A\d+\?from=filter&spread=commsearch_p&position=\d+&kwtype=filter&now_time=\d+)"',
                content)
            # title
            urlSpD = BeautifulSoup(content1, "html.parser")
            titleListTemp = urlSpD.find_all('a', class_='houseListTitle')
            titleList = list(map(lambda x: x.text, titleListTemp))
            titleList = list(map(lambda x: x.strip(), titleList))
            # print(titleList)
            for url in urlList:
                # print('小的url:',url)
                try:
                    urlHtml = requests.get(url=url, headers=self.header)
                    if urlHtml.status_code == 200:
                        urlContent = urlHtml.text
                    elif urlHtml.status_code == 403:
                        print(403,urlHtml.url)
                    else:
                        print("出错", urlHtml.status_code,urlHtml.url)

                    # 每个url树的解释树
                    urlSp = BeautifulSoup(urlContent, "html.parser")
                    houseInfoTree = urlSp.find_all('ul', class_='houseInfo-detail-list clearfix')
                    houseInfoTree = houseInfoTree[0].text
                    # print(houseInfoTree)
                    houseinfoLi = str(houseInfoTree).split('\n')

                    houseInfo = []
                    for i in houseinfoLi:
                        if i == '' or i.endswith("：") or i == '\ue003' or i == '  ':
                            continue
                        else:

                            if '\t' in i:
                                i = i.replace('\t', ' ').strip()
                                if i == '':
                                    continue
                            houseInfo.append(i.strip())
                    # 字符串的清洗
                    def dataClear(li=[]):

                        try:
                            li.pop()
                            li[1] = ''.join(li[1:4])
                            li[5] = ''.join(li[5:8])
                            del li[6:8]
                            del li[2:4]
                        #         if li[-1] == '是':
                        #             li[-1] = '唯一'
                        #         else:
                        #             li[-1] = '不唯一'
                        #         houseInfo[-1] = ''.join(li[-2:])
                        #         del houseInfo[-2]
                        except Exception as ex:
                            print(ex)
                        return li

                    #
                    houseInfo = dataClear(houseInfo)
                    houseInfo.append(url)
                    num = urlList.index(url)
                    houseInfo.insert(0, titleList[num])
                    print(houseInfo)
                    self.resultList.append(houseInfo)

                except Exception as ex:
                    print("somenthing wrong!：", ex)

            # print(self.resultList)

    def dataSave(self):
        feature = ['title', 'community', 'ApartmentTpye', 'SingelPrice/m2', 'address', 'houseSize', 'down-payment',
                   'year',
                   'toward',
                   'pricePerMonth', 'houseTpye', 'layer', 'decorate', 'rightLimit', 'lift', 'houseAge', 'rightProperty',
                   'SingelHouse', 'detailUrl']
        try:
            with open('./Anjuke1.csv', mode='a', encoding="utf-8", newline='') as f:
                f_csv = csv.writer(f)
                # f_csv.writerow(feature)
                f_csv.writerows(self.resultList)
        except IOError as IOex:
            print(IOex)


if __name__ == '__main__':
    myAjuke = ArawlSpider()
    myAjuke.dataCrawl()
    # myAjuke.dataSave()
