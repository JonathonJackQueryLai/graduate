#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 将 IP 存进CVS
import pymongo
import csv

class Revenge_first(object):
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

    def find(self, _all=False):
        if _all:
            return self.col_name.find()
        else:
            return self.col_name.find_one()
    # def find(self):
    #     return self.col_name.find()


if __name__ == '__main__':
    MM = Revenge_first('IP', 'store')
    bigDict = MM.find()
    print('hello')
    # print(type(bigDict))
    # for i in bigDict:
    for i in bigDict:
        # print(i)
        print(bigDict[i])
    # res = list(bigDict.values())
    # print(res)
    # print((bigDict))
    # with open('./IP.csv') as ff:
    #     ff.write()