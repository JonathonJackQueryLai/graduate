#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 赶集网二手房
import csv
import re

import requests
from bs4 import BeautifulSoup

st = """
_gl_tracker	{"ca_source":"www.baidu.com","ca_name":"-","ca_kw":"-","ca_id":"-","ca_s":"seo_baidu","ca_n":"-","ca_i":"-","sid":52797196194}
bizs	[]
citydomain	jiangmen
ganji_login_act	1555689447728
ganji_uuid	4717082969845639536005
ganji_xuuid	9ac1ef3c-1d46-48a8-d22f-cb2a08813037.1542610963267
GanjiLoginType	0
GANJISESSID	ec55spljtmnqk2tqgttga72d58
GanjiUserInfo	{"user_id":808407255,"email":"","username":"#t_808407255","user_name":"#t_808407255","nickname":""}
GanjiUserName	#t_808407255
last_name	#t_808407255
lg	1
sscode	azFbltuMP7djmXf9azaD0/hm
supercookie	BQN4AQN3ZwH1WTIuZwplL2MzZQWvMzL5MTMxZ2D4L2D2AmV2ZGOuAwAxL2Z1ZQt4Awt=
username_login_n	15815773235
xxzl_deviceid	D5Ti4dxMODQSef1gs+TKl/vU6dwp+P+PDaetLL5DMK4ZVNdyeUKqOSI+vC6ArquI
xxzl_smartid	1026544797a343c107a6d36cf9d7a474
"""


def firfox_cookies_copy_format2dict(copy_format_cookies: str) -> dict:
    """

    :param copy_format_cookies: cookies 复制出格式存在空格和制表符的字符串，可使用\"""来表达承字符串
    :return:  dict
    """
    item = copy_format_cookies.split("\n")
    ret_dict = {}
    for i in item:
        if not i:
            continue
        k, v = i.split('\t', maxsplit=1)
        ret_dict.update([(k, v)])
    return ret_dict
"""
    community,ApartmentTpye,P/m2,address,houseSize,down-payment,year,toward,pricePerMonth,houseTpye,layer,decorate,SingelLabel,detailUrl
community,ApartmentTpye,P/m2,address,houseSize,down-payment,year,toward,pricePerMonth,houseTpye,layer,decorate,SingelLabel,detailUrl
"""

# 出现反爬虫情况 未解决
class GanSpider(object):
    def __init__(self):
        self.__name = '赶集网二手网'
        self.resultList = []
        self.start_url = 'http://jiangmen.ganji.com/ershoufang/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
            'GANJISESSID': 'ec55spljtmnqk2tqgttga72d58',
            'GanjiLoginType': '0',
            'GanjiUserInfo': '{"user_id":808407255,"email":"","username":"#t_808407255","user_name":"#t_808407255","nickname":""}',
            'GanjiUserName': '#t_808407255',
            '_gl_tracker': '{"ca_source":"www.baidu.com","ca_name":"-","ca_kw":"-","ca_id":"-","ca_s":"seo_baidu","ca_n":"-","ca_i":"-","sid":52797196194}',
            'bizs': '[]',
            'citydomain': 'jiangmen',
            'ganji_login_act': '1555689447728',
            'ganji_uuid': '4717082969845639536005',
            'ganji_xuuid': '9ac1ef3c-1d46-48a8-d22f-cb2a08813037.1542610963267',
            'last_name': '#t_808407255',
            'lg': '1',
            'sscode': 'azFbltuMP7djmXf9azaD0/hm',
            'supercookie': 'BQN4AQN3ZwH1WTIuZwplL2MzZQWvMzL5MTMxZ2D4L2D2AmV2ZGOuAwAxL2Z1ZQt4Awt=',
            'username_login_n': '15815773235',
            'xxzl_deviceid': 'D5Ti4dxMODQSef1gs+TKl/vU6dwp+P+PDaetLL5DMK4ZVNdyeUKqOSI+vC6ArquI',
            'xxzl_smartid': '1026544797a343c107a6d36cf9d7a474'
        }
        self.feature = ['urLDetail', 'title', 'realese-time', 'price', 'houseType', 'houseSize', 'toward', 'layer',
                        'buildingYear',
                        ' propertyRight', 'decorate', 'community', 'address']

    def __repr__(self):
        return self.__name

    # 这个是爬东西用的。
    def dataCrawl(self):
        urlList = set()
        for i in range(1, 11):
            rangeUrl = self.start_url + 'pn{0}/'.format(i)
            print('[{0}]:{1}'.format(i, rangeUrl))
            html = requests.get(url=rangeUrl, headers=self.headers)
            if html.status_code == 200:
                content = html.text

            tempList = re.findall(
                r'(//jiangmen.ganji.com/ershoufang/\d+x.shtml)',
                content)

            for i in tempList:
                # print(i)
                i = '{0}{1}'.format('http:', i)
                urlList.add(i)

            #  爬取每个url的内容
            houseInfo = []

            for url in urlList:
                # print(url)
                try:
                    houseInfo.append(url)
                    urlHtml = requests.get(url=url, headers=self.headers)
                    if urlHtml.status_code == 200:
                        urlContent = urlHtml.text
                        print(urlHtml.url)
                    elif urlHtml.status_code == 403:
                        print('403:',urlHtml.url)

                    else:
                        print("出错：", urlHtml.status_code)
                    # 每个url树的解释树
                    urlSp = BeautifulSoup(urlContent, "html.parser")
                    # print(urlSp)
                    houseInfoTree = urlSp.find_all('div', class_='card-top')
                    houseInfoTree = houseInfoTree[0].text
                    houseinfoLi = str(houseInfoTree).split('\n')
                    # print(houseinfoLi)
                    houseInfoTemp = []
                    for i in houseinfoLi:
                        if '\xa0' in i or i == '\ue003' or i == '':
                            continue
                        else:
                            if '\t' in i:
                                i = i.replace('\t', ' ').strip()
                                if i == '':
                                    continue
                            houseInfoTemp.append(i.strip())
                            # print(houseInfoTemp)
                    print(houseInfoTemp)
                    self.resultList.append(houseInfoTemp)
                    # print(self.resultList)

                except Exception as ex:
                    raise ex
                    print("something wrong:", ex)

    def dataSave(self):
        feature = ['community', 'ApartmentTpye', 'P/m2', 'address', 'houseSize', 'down-payment', 'year',
                   'toward',
                   'pricePerMonth', 'houseTpye', 'layer', 'decorate', 'SingelLabel', 'detailUrl']
        # with open('./Anjuke.csv', mode='w', encoding="utf-8", errors='ignore') as f:
        with open('./gani.csv', mode='a', encoding="utf-8", errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(feature)
            f_csv.writerows(self.resultList)


if __name__ == '__main__':
    myGS = GanSpider()
    myGS.dataCrawl()
    myGS.dataSave()
