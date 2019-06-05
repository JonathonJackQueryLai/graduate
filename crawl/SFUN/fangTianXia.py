#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 江门市二手房爬取

import concurrent
import csv
import queue
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as F_TimeoutError
from queue import Empty
from threading import Lock

import requests
from bs4 import BeautifulSoup


class Spider(object):
    lock = Lock()

    def __init__(self):
        self.__name = '二手房爬虫'
        self.urlList = queue.Queue(10)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
        self.start_url = 'https://jm.esf.fang.com/house/i3{0}/'
        self.resultList = []

    def crawlInfo(self):
        def craw(self):
            # 保证线程及时清理
            with ThreadPoolExecutor(max_workers=4) as executor:

                futures = [executor.submit(requests.get, url=url, headers=self.header) for url in
                           [self.start_url.format(u) for u in range(1, 101)]]
                try:
                    for future in concurrent.futures.as_completed(futures):
                        html = future.result()
                        print(html.url)
                        content = html.text
                        # 防止数据感染
                        content1 = content
                        soup = BeautifulSoup(content1, 'lxml')
                        houseInfo = soup.find_all('dl', class_='clearfix')
                        self.urlList.put((houseInfo, soup))
                except F_TimeoutError:
                    print("### timeout ###")
                    self.urlList.put((None, None))
                self.urlList.put((None, None))

        # threading.Thread(target=getInfo_loop, args=(self,)).start()
        threading.Thread(target=craw, args=(self,)).start()
        st = time.time()
        while True:
            try:
                houseInfo_, soup_ = self.urlList.get(timeout=5)
            except Empty:
                print('-', end='', flush=True)
                continue
            print('.', end='', flush=True)
            if houseInfo_ is None and soup_ is None:
                break
            else:
                self._getInfo(houseInfo_, soup_)
        print(time.time() - st)

    def _getInfo(self, houseInfo, soup):
        """
        解析 获取 数据并写入文件
        :param houseInfo:  bs4 resultSet
        :param soup: bs4 class
        :return:
        """
        try:
            for infoItem in houseInfo:
                # url
                # print(infoItem)
                # https://jm.esf.fang.com/chushou/3_346277977.htm?channel=1,2&psid=2_1_60
                urlPartern = re.compile(r'<a data_channel="1,2" href="(/chushou/.*?.htm)" ps="(.*?)" target="_blank">')
                urlstr = re.findall(urlPartern, string=str(infoItem))
                if urlstr == []:
                    continue
                url = 'https://jm.esf.fang.com{0}?channel=l,2&psid={1}'.format(urlstr[0][0], urlstr[0][1])
                print(url)
                # url

                # 标题
                # print(infoItem)
                titlePartern = re.compile('<span class="tit_shop">(.*?)</span>')
                title = re.findall(titlePartern, string=str(infoItem))
                if title == []:
                    title.append('无')
                else:
                    title = title[0]
                # print('title：', len(title))
                # tempList.append(title[0])
                # print('title：', title)

                # 每个平方的价格
                pricePartern = re.compile('(\d+元)/�O')
                price = re.findall(pricePartern, string=str(infoItem))
                if price == []:
                    price.append('wu')
                else:
                    price = price[0] + '每平方米'
                    # print('price', price)
                    # tempList.append(price[0])
                    # print('price:', len(price))
                # 总价
                totalPricePartern = re.compile('<span class="red"><b>(.*?)</b>万</span>')
                totalPrice = re.findall(totalPricePartern, string=str(infoItem))
                if totalPrice == []:
                    totalPrice.append('null')
                else:
                    totalPrice = totalPrice[0] + '万元'
                # print(totalPrice)
                # tempList.append(totalPrice[0])
                # print('totalPrice:', len(totalPrice))

                houseType = re.findall(r"\d室\d厅", string=str(infoItem))
                houseSize = re.findall(r'(\d+)�O', string=str(infoItem))
                toward = re.findall(r'..向', string=str(infoItem))
                startYear = re.findall('\d+年建', string=str(infoItem))
                layer = re.findall('.层（共\d+层）', string=str(infoItem))
                if houseType == []:
                    houseType.append('null')
                else:
                    houseType = houseType[0]

                if houseSize == []:
                    houseSize.append('null')
                else:
                    houseSize = houseSize[0] + '平方米'
                if toward == []:
                    toward.append('无向')
                toward = toward[0].strip('>')
                if startYear == []:
                    startYear.append('null')
                else:
                    startYear = startYear[0]

                if layer == []:
                    layer
                else:
                    layer = layer[0]

                # 小区和 地点
                addressList = []
                communityList = []
                NMInfo = soup.find_all('p', class_='add_shop')
                communityPartern = re.compile(r'title="(.*?)"')
                addressPartern = re.compile(r'<span>(.*?)</span>')
                community = re.findall(communityPartern, str(NMInfo[0]))
                address = re.findall(addressPartern, str(NMInfo[0]))
                community = community[0]
                address = address[0]
                # print(address)
                # print(community)
                tempList = [title, price, totalPrice, houseType, houseSize, startYear, toward,
                            layer, address, community, url]

                # 特征标签
                label = re.findall(r'<span class="colorPink note">(.*?)</span>', string=str(infoItem))
                if label != []:
                    tempStr = ''
                    for i in label:
                        tempStr += i
                    tempList.append(tempStr)
                # print(label)
                # print('tempList:', tempList)
                self.resultList.append(tempList)
                # print(self.resultList)

        except Exception as ex:
            print("something wrong!：", ex)
            raise ex

    def dataStore(self):

        feature = ['title', 'perPrice', 'totalPrice', 'houseType', 'houseSize', 'startYear', 'toward', 'layer',
                   'address',
                   'community', 'label', 'url']
        with open('./SFUN1.csv', mode='w', encoding="utf-8", errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(feature)
            f_csv.writerows(self.resultList)
            # for row in Spider.resultList:
            #     f_csv.writerows()


if __name__ == '__main__':
    mySpider = Spider()
    mySpider.crawlInfo()
    # mySpider.dataStore()
