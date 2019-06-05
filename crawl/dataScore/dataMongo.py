#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : mongo
import pandas as pd
import pymongo
import pandas as pd

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

    def find(self):
        return self.col_name.find()

    def findone(self, _all=True):

        return self.col_name.find_one()


class WRcsv(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = pd.read_csv(filePath)

    def readCsvAddress(self):
        addressList = self.data['address']
        return addressList

    def readCsvCommunity(self):
        communityList = self.data['community']
        return communityList

    def writeCvstoMongo(self, filePath):
        # 输入路径
        data = pd.read_csv(filePath)
        dataList = []
        dataDict = {}
        for i in data.itertuples(index=True, name=None):
            dataList.append(i)
        for i in dataList:
            dataDict[str(i[0])] = i[1::]

    # F:\Users\python\PycharmProjects\webAddress_New\crawl\Anjuke\Anjuke.csv
# df = pd.read_csv(r'F:\Users\python\PycharmProjects\webAddress_New\crawl\Anjuke\SFUN1.csv')
# df1 = pd.read_csv('SFUN1.csv')

# tempList1 = []
# for i in range(6000):
#     tempList1.append(str(i))
# # #
# df1 =df.copy()
# df['index'] = tempList1
# #
# df_new = pd.concat([df['index'],df1],
#                        axis=1)
# print(df_new)
# df_new.to_csv("SFUN1.csv", columns=df_new.iloc[0].keys(),index=None)

myMongo = MonDb('house', 'Anjuke1')
mySFUN = MonDb('house', 'SFUN')
# for i in range(len(df1)):
#     dt = {}
#     a= df1.iloc[i].tolist()
#     print(a)
#     a[0] = str(a[0])
#     dt[str(i)] = a
#     mySFUN.insert(dt)


# topicList = list(df1.head(n=0))
# # print(myMongo.find()[:100].next())
# a = []
# def insertToMongo(df):
#     for i in range(len(df)):
#         dit = {}
#         x = df.iloc[i].tolist()
#         x[0] = int(x[0])
#         dit[str(i)]=dict(zip(topicList,x))
#         print(dit)
#         myMongo.insert(dit)
# insertToMongo(df1)

# print(a)
# print(myMongo.find().next())




# myMongo.

myWRcsv = WRcsv(r'F:\Users\python\PycharmProjects\webAddress_New\crawl\Anjuke\Anjuke1.csv')
AddressList = list(myWRcsv.readCsvAddress())
communityList = list(myWRcsv.readCsvCommunity())
detailList = []

for tempList in zip(AddressList,communityList):
    tempList = list(tempList)
    tempList.insert(1,'－')
    temStr = ''
    for i in tempList:
        temStr = temStr + i

    detailList.append(temStr)

# print(detailList)
Add_ComList = list(set(detailList))





    # myMongo.insert(read_cvs(r'../Anjuke/Anjuke1.csv'))
    # findRes = myMongo.find()
    # findRes = findRes.next()
    #
    # for i in findRes.values():
    #     print(i)
