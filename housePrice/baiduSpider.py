#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 12:12
# @Author  : @乌鸦坐飞机
# Description   :

import random

import pandas
import requests


class BaiduSpider(object):
    def __init__(self, pathFile=''):
        self.akList = ['tH5K6VVZMS6GRlGeNsBjmyImFu5Fz2ip',
                   'n3dEB2E9nKLfDb4avibAMBd9fC2iTkt9',
                   'PvROomI67Xk4WIiafWXxiWs6K0D4msns',
                   '1xakMypp6RXlFOHCiBG5TIfOFICPT6es',
                   'Z9GiZqjT56e6Lkr0O4Ber2f2KfGdb68E',
                   'yCMIuhugP5dG9wujCpnxT76V1ulzB76O',
                   'YVzetnTGHn8eMNVIkseR0V5oqRBxTU5W',
                   '2dkHWlM9pQdyydvll3eQN8oLDTOs0avs'
                   'pFRnwVqmd08gWoNgwhsL75kPfWwBRzId',
                   'LAg428CW5xX8wbaGae8nVUEIXvM9E01s',
                   ]
        seed = random.randint(1, 10)
        self.sUrl = 'http://api.map.baidu.com/geocoder/v2/?address=江门 \
                    中天国际&output=json&ak=%s'%self.akList[seed]
        self.houseDATA = pandas.read_csv(pathFile)

    def run(self):
        html = requests.get(url=self.sUrl)
        try:
            if html.status_code == 200:
                cont = html.text
                print(cont)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    myBS = BaiduSpider(pathFile='F:\\Users\python\PycharmProjects\webAddress_New\crawl\SFUN\SFUN.csv')
    print(myBS.houseDATA['community'])
    myBS.run()