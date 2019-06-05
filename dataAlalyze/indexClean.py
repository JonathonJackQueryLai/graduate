#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 23:43
# @Author  : @乌鸦坐飞机
# Description   :
# from housePrice.views import
import collections
import pandas
import re
from crawl.dataScore.dataMongo import myMongo
import joblib
import numpy as np
from sklearn import metrics
import re
from crawl.dataScore.dataMongo import detailList


class IndexCleaner(object):
    def __init__(self, indexList=[]):
        self.indexList = indexList
        self.headers = ['cAaGet', 'towardGet', 'housetypeGet', 'liftGet', 'floorGet', 'rightGet', 'decorateGet',
                        'housesizeGet', 'totalfloorGet', 'singleGet']

        self.dic = dict(map(lambda x, y: [x, y], self.headers, self.indexList))
        # self.df = pd.DataFrame(self.dic)
        print(self.dic)

    def findNumber(self, reStr, sourceStr):
        result_list = re.findall(reStr, sourceStr)
        if len(result_list):
            return result_list[0]
        else:
            return 0

    def houseSizeClean(self):
        tempStr = self.dic['housesizeGet']
        # 处理 去掉平方米的方法
        houseSize = int(tempStr)
        if houseSize < 50:
            houseSize = '1'
        elif houseSize < 100:
            houseSize = '2'
        elif houseSize < 150:
            houseSize = '3'
        elif houseSize < 200:
            houseSize = '4'
        else:
            houseSize = '5'
        return int(houseSize)

    def liftGetClean(self, floorstr='', liftGetstr=''):
        floorstr = self.dic['floorGet']
        liftGetstr = self.dic['liftGet']
        if liftGetstr == '有':
            liftGetstr = 1
        elif liftGetstr == '无':
            if int(floorstr) > 8:
                liftGetstr = 0
            else:
                liftGetstr = 1

        return liftGetstr

    def decorateGetClean(self):
        tempStr = self.dic['decorateGet']
        if tempStr == '豪华装修':
            tempStr = 2
        elif tempStr == '精装修':
            tempStr = 1
        elif tempStr == '毛坯' or tempStr == '简单装修':
            tempStr = 0
        else:
            tempStr = 0

        return tempStr

    def singleGetClean(self):
        tempStr = self.dic['singleGet']
        if tempStr == '是':
            tempStr = 1
        elif tempStr == '否':
            tempStr = 0
        else:
            tempStr = 0

        return tempStr

    def rightGetClean(self):
        tempStr = self.dic['rightGet']
        if tempStr == '满五年':
            tempStr = 2
        elif tempStr == '满二年':
            tempStr = 1
        else:
            tempStr = 0
        return tempStr

    def towardGetclean(self):
        tempStr = self.dic['towardGet']
        indexTable = ['东', '东北', '东南', '东西', '北', '南', '南北', '西', '西北', '西南']
        cleanList = []
        for i in indexTable:
            if tempStr == i:
                i = 1
            else:
                i = 0
            cleanList.append(i)
        return cleanList

    def housetypeGetclean(self):
        tempStr = self.dic['housetypeGet']
        room = int(self.findNumber('([0-9]*)室', tempStr))
        hall = int(self.findNumber('([0-9]*)厅', tempStr))
        restroom = int(self.findNumber('([0-9]*)卫', tempStr))
        return [room, hall, restroom]

    # 8 41 494 629
    def cAaGetClean(self):
        tempStr = self.dic['cAaGet']

        def MultiIndex():
            cityList = []
            regionList = []
            streetList = []
            communityList = []
            for item in detailList:
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
            # cityWeight = collections.Counter(cityList)
            # regionWeight =collections.Counter(regionList)
            # streetWeight = collections.Counter(streetList)
            # communityWeight = collections.Counter(communityList)

            return (cityWeight, regionWeight, streetWeight, communityWeight)

        cityList = []
        regionList = []
        streetList = []
        communityList = []
        tempList = tempStr.split('－')
        cityList.append(tempList[0])
        regionList.append(tempList[1])
        streetList.append(tempList[2])
        communityList.append(tempList[3])
        indexTable = MultiIndex()
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
        tailNum = formula * 10 - int(formula * 10)
        formula = formula * 10
        if tailNum >= 0.5:

            formula = (int(formula) + 1) / 10
        else:
            formula = (int(formula) - 1) / 10
        # print(cityValue, regionValue, streetValue, communityValue)
        return formula


tLi = [
    '开平市－开平周边－寺前西路83号－康城 ',
    '南',
    '3室2厅1卫',
    '有',
    '8',
    '满五年',
    '精装修',
    '88',
    '10',
    '是',
]


def runClean(li=[]):
    # room,hall,restroom,houseSize,elevator,decorate,houseAge,SingelHouse,cAa,东,东北,东南,东西,北,南,南北,西,西北,西南
    reslist = []
    myIndexCleaner = IndexCleaner(li)
    cAaGetRes = myIndexCleaner.cAaGetClean()
    decorateGetRes = myIndexCleaner.decorateGetClean()
    houseSizeGetRes = myIndexCleaner.houseSizeClean()
    housetypeGetRes = myIndexCleaner.housetypeGetclean()
    liftGetRes = myIndexCleaner.liftGetClean()
    rightGetRes = myIndexCleaner.rightGetClean()
    towardGetRes = myIndexCleaner.towardGetclean()
    singleGetRes = myIndexCleaner.singleGetClean()
    reslist.extend(housetypeGetRes)
    reslist.append(houseSizeGetRes)
    reslist.append(liftGetRes)
    reslist.append(decorateGetRes)
    reslist.append(rightGetRes)
    reslist.append(singleGetRes)
    reslist.append(cAaGetRes)
    reslist.extend(towardGetRes)
    # #载入模型

    test_y = np.array([reslist])
    # x = x.reshape(-1, 1)
    model_DT = (joblib.load(r'F:\Users\python\PycharmProjects\webAddress_New\dataAlalyze\dr_model.pickle'))
    model_RT = (joblib.load(r'F:\Users\python\PycharmProjects\webAddress_New\dataAlalyze\regr_model.pickle'))
    model_regr = (joblib.load(r'F:\Users\python\PycharmProjects\webAddress_New\dataAlalyze\RFR_model.pickle'))
    result_DT = model_DT.predict(test_y)
    result_RT = model_RT.predict(test_y)
    result_regr = model_regr.predict(test_y)
    # 做不了动态匹配
    # score_DT = float((metrics.explained_variance_score(test_y, result_DT), 2)[0])
    # score_RT = float((metrics.explained_variance_score(test_y, result_RT), 2)[0])
    # score_regr = float((metrics.explained_variance_score(test_y, result_regr), 2)[0])
    # temp = max(score_DT,score_regr,score_RT)
    # if temp == score_DT:
    #     return result_DT
    # elif temp == score_RT:
    #     return result_RT
    # elif temp == score_regr:
    #     return result_regr
    # else:
    #     return result_RT
    return (result_RT)

#
# print(runClean(tLi))

def result_refer(addressString =''.strip()):
    df = pandas.read_csv(r"F:\Users\python\PycharmProjects\webAddress_New\crawl\Anjuke\Anjuke1.csv")
    tempAddress = addressString.split('－')[:3]
    address = '－'.join(tempAddress)
    numList = []
    priceList = []
    for i in range(len(df['address'])):
        if df['address'].iloc[i] == address:
            numList.append(i)
    for num in range(len(numList)):
        numField = re.findall(r'\d+',string=str(df.iloc[num]['perPrice']))
        priceList.append(numField[0])

    def Get_Average(li):
        sum = 0
        for item in li:
            sum += int(item)
        if len(li) == 0:
            return 7586.0
        return sum / len(li)
    refer_price = Get_Average(priceList)
    return refer_price
# print(result_refer('开平市－开平周边－寺前西路83号－康城 '))