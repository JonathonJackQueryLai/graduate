#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/9 15:42
# @Author  : @乌鸦坐飞机
# Description   :

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   :
import re

import pandas as pd


def printField(df):
    for x, y in enumerate(list(df.iloc[0].keys()), start=1):
        print(x, y)


def findNumber(reStr, sourceStr):
    result_list = re.findall(reStr, sourceStr)
    if len(result_list):
        return result_list[0]
    else:
        return 0


if __name__ == '__main__':
    # 19 个 字段
    # df = pd.read_csv('../crawl/Anjuke/Anjuke1.csv')
    df = pd.read_csv('../crawl/SFUN/SFUN.csv')

    # title 去除
    if 'title' in df:
        df = df.drop(['title', 'detailUrl', 'houseTpye', 'rightLimit', 'rightProperty', 'down-payment', 'startYear',
                      'pricePerMonth'], axis=1)
    # print(len(df[df['ApartmentTpye'] == df['ApartmentTpye']]))

    # 处理三室两厅的事情
    ApartmentTpyeList = []
    for i in range(len(df)):
        sizeType = df['ApartmentTpye'].iloc[i]
        sizeType_dict = dict(
            room=findNumber('([0-9]*)室', sizeType),
            hall=findNumber('([0-9]*)厅', sizeType),
            restroom=findNumber('([0-9]*)卫', sizeType)
        )
        ApartmentTpyeList.append(sizeType_dict)
    df1 = pd.DataFrame(ApartmentTpyeList, columns=ApartmentTpyeList[0].keys())
    df = df.drop(['ApartmentTpye'], axis=1)

    # 处理 去掉平方米的方法
    df2 = df['houseSize']
    for i in range(len(df)):
        df2.iloc[i] = df['houseSize'].iloc[i].strip('平方米')
    df['houseSize'] = df2

    #   处理perPrice 去掉元/m²
    df2 = df['perPrice']
    for i in range(len(df)):
        df2.iloc[i] = df['perPrice'].iloc[i].strip('每平方米')
    df['perPrice'] = df2

    #  toward
    df4 = pd.get_dummies(df['toward'])
    # print(df4)
    df = pd.concat([df.drop(['toward'], axis=1), df4], axis=1)

     # height
    df5 = df['floor']
    for i in range(len(df)):
        df5.iloc[i] = re.findall(r'\d+',str(df['floor'].iloc[i]))[0]
    df['floor'] = df5

    # decorate 装修
    df6 = pd.get_dummies(df['decorate'])
    df = pd.concat([df.drop(['decorate'], axis=1), df6], axis=1)

    # lift
    df7 = df['lift']
    for i in range(len(df7)):
        if df7.iloc[i] == '有':
            df7.iloc[i] = 1
        else:
            df7.iloc[i] = 0
    df['lift'] = df7

    # houseAge
    df8 = df['houseAge']

    printField(df)

    #