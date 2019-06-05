#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/26 14:41
# @Author  : @乌鸦坐飞机
# Description   :
import requests

# {#http://api.map.baidu.com/?qt=gc&wd=中天国际&cn=江门&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk62300#}
# html = requests.get(url='http://localhost:63342/AIMap/housePrice/templates/%E5%9F%BA%E8%AE%BE.html?_ijt=4c44knq3k02brfv0q1p4090943')
# data = pd.read_csv('..\crawl\Anjuke\Anjuke1.csv')
# for i in range(len(data)):
#     print(data.iloc[i]['community'])
#     print(data.iloc[i]['community'])
#     print(data.iloc[i]['community'])
#     print(data.iloc[i]['community'])
#     break
# <a href="javascript:window.opener=null;window.open('','_self');window.close();">关闭</a>
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
}
html = requests.get(url='https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam&serialID=9fd34110c7a80f9cf57058c2836bd820_1a5323c46e7b4642a2ee97388ec87da8&history=aHR0cHM6Ly93d3cuYW5qdWtlLmNvbS8%3D',headers=header)
cont = html.text
print(html.url)