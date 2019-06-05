#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   :
import collections
import re
import time

import pandas as pd


def printField(df):
    '''
    :param df:
    :return:
    '''
    for x, y in enumerate(list(df.iloc[0].keys()), start=1):
        print(x, y)


def findNumber(reStr, sourceStr):
    result_list = re.findall(reStr, sourceStr)
    if len(result_list):
        return result_list[0]
    else:
        return 0


# 将地址和小区分成四块
def MultiIndex():
    cityList = []
    regionList = []
    streetList = []
    communityList = []
    for item in cAaList:
        tempList = []
        tempList = item.split('－')
        cityList.append(tempList[0])
        regionList.append(tempList[1])
        streetList.append(tempList[2])
        communityList.append(tempList[3])
    cityListIndex = list(set(cityList))
    regionListIndex = list(set(regionList))
    streetListIndex = list(set(streetList))
    communityListIndex = list(set(communityList))
    cityListIndex.sort(key=cityList.index)
    regionListIndex.sort(key=regionList.index)
    streetListIndex.sort(key=streetList.index)
    communityListIndex.sort(key=communityList.index)
    cityWeight = dict(collections.Counter(cityList))
    regionWeight = dict(collections.Counter(regionList))
    streetWeight = dict(collections.Counter(streetList))
    communityWeight = dict(collections.Counter(communityList))
    return (cityWeight, regionWeight, streetWeight, communityWeight)
    # cityWeight = collections.Counter(cityList)
    # regionWeight =collections.Counter(regionList)
    # streetWeight = collections.Counter(streetList)
    # communityWeight = collections.Counter(communityList)
    # print (cityListIndex.__len__(), regionListIndex.__len__(), streetListIndex.__len__(), communityListIndex.__len__())

    # return (cityList, regionList, streetList, communityList)


# 就算出 communit
def weightCal(pointStr=''):
    '''
    :param pointStr:
    :return:
    '''
    #  cityWeight, regionWeight, streetWeight, communityWeight
    indexTable = MultiIndex()
    tempList = pointStr.split('－')
    cityIndexKey = tempList[0]
    regionIndexKey = tempList[1]
    streetIndexKey = tempList[2]
    communityIndexKey = tempList[3]
    cityValue = 0
    regionValue = 0
    streetValue = 0
    communityValue = 0
    for itemKey in indexTable[0].keys():
        cityValue = 100
        if cityIndexKey == itemKey:
            cityValue = indexTable[0][itemKey]
            break

    for itemKey in indexTable[1].keys():

        regionValue = 50
        if regionIndexKey == itemKey:
            regionValue = indexTable[1][itemKey]
            break

    for itemKey in indexTable[2].keys():
        streetValue = 50
        if streetIndexKey == itemKey:
            streetValue = indexTable[2][itemKey]
            break

    for itemKey in indexTable[3].keys():
        communityValue = 1
        if communityIndexKey == itemKey:
            communityValue = indexTable[3][itemKey]
            break
    formula = cityValue / 989 + regionValue / 342 + streetValue / 90 + communityValue / 67 + 1
    tailNum = formula * 100 - int(formula * 100)
    formula = formula * 100
    if tailNum >= 0.5:

        formula = (int(formula) + 1) / 100
    else:
        formula = (int(formula) - 1) / 100

    # print(cityValue, regionValue, streetValue, communityValue)
    return formula


if __name__ == '__main__':

    # 19 个 字段
    df = pd.read_csv('../crawl/Anjuke/Anjuke1.csv')
    # title 去除

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
    # 处理 去掉平方米的方法
    df2 = df['houseSize'].copy()
    for i in range(len(df2)):
        size = float(df['houseSize'].iloc[i].strip("平方米"))
        if size < 50:
            df2.iloc[i] = '1'
        elif size < 100:
            df2.iloc[i] = '2'
        elif size < 150:
            df2.iloc[i] = '3'
        elif size < 200:
            df2.iloc[i] = '4'
        else:
            df2.iloc[i] = '5'
    df['houseSize'] = df2

    # 处理perPrice 去掉元/m² 是一个target
    df2 = df['perPrice'].copy()
    for i in range(len(df)):
        df2.iloc[i] = df['perPrice'].iloc[i].strip('元/m²').strip('')
    df['perPrice'] = df2

    #  toward
    df4 = pd.get_dummies(df['toward'])
    # print(df4)
    # df44 = pd.concat([df.drop(['toward'], axis=1), ds], axis=1)

    # height
    df5 = df['floor'].copy()
    for i in range(len(df)):
        df5.iloc[i] = re.findall(r'\d+', str(df['floor'].iloc[i]))[0]
    df['height'] = df5

    # # lift
    # df7 = df['lift'].copy()
    # for i in range(len(df7)):
    #     if df7.iloc[i] == '有':
    #         df7.iloc[i] = 1
    #     else:
    #         df7.iloc[i] = 0
    # df['lift'] = df7

    ele_list = []
    for i in range(len(df['height'])):
        heightItem = df['height'].iloc[i]
        elevator = 1 if int(heightItem) >= 8 else 0
        ele_dict = {'elevator': elevator}
        ele_list.append(ele_dict)
    df21 = pd.DataFrame(ele_list)

    # decorate 装修
    df6 = df['decorate'].copy()
    for i in range(len(df6)):

        if df6.iloc[i] == '豪华装修':
            df6.iloc[i] = 2
        elif df6.iloc[i] == '精装修':
            df6.iloc[i] = 1
        elif df6.iloc[i] == '毛坯' or df6.iloc[i] == '简单装修':
            df6.iloc[i] = 0
        else:
            df6.iloc[i] = 0
    df['decorate'] = df6

    # houseAge
    df8 = df['houseAge'].copy()
    for i in range(len(df8)):
        if (df8.iloc[i] == '满五年'):
            df8.iloc[i] = 2
        elif (df8.iloc[i] == '满二年'):
            df8.iloc[i] = 1
        elif (df8.iloc[i] == '不满二年'):
            df8.iloc[i] = 0
        else:
            df8.iloc[i] = 0
    df['houseAge'] = df8

    # SingelHouse
    df9 = df['SingelHouse'].copy()
    for i in range(len(df8)):
        if (df9.iloc[i] == '是'):
            df9.iloc[i] = 1
        elif (df9.iloc[i] == '否'):
            df9.iloc[i] = 0
        else:
            df9.iloc[i] = 0
    df['SingelHouse'] = df9

    #  community &address
    df10 = df['community'].copy()
    df11 = df['address'].copy()
    df.drop(['community', 'address'], axis=1)
    cAaList = []
    for x, y in zip(df10, df11):
        temp = ''
        temp = y + '－' + x
        cAaList.append(temp)
    df['cAa'] = cAaList
    # print(MultiIndex())
    # print(MultiIndex()[3].__len__())

    for i in range(len(df['cAa'])):
        pointNum = weightCal(df['cAa'].iloc[i])

        if pointNum > float(5.0):
            pointNum = float(5.0)
        df['cAa'].iloc[i] = pointNum
    print(df['cAa'])
    start = time.time()
    df_new = pd.concat([df['perPrice'], df1, df['houseSize'], df21, df['decorate'], df['houseAge'], df[
        'SingelHouse'], df['cAa'], df4,
                        ],
                       axis=1)
    df_new.to_csv("myClean3.csv", columns=df_new.iloc[0].keys())
    print(time.time() - start)
