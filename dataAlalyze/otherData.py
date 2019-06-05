#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/7 13:58
# @Author  : @乌鸦坐飞机
# Description   :


'''
原来的数据总共有15列：分别为：标题title、价格price、首付downPayment、
户型sizeType、面积size、单价unitPrice、朝向orientation、楼层floor、
装修decoration、社区community、区域region、学校school、房屋详情houseDetail、
核心卖点keySellingPoint、配套设施equipment
'''
'''
进行简单的房价预测不需要用到文本识别和语义分析，因此不需要用到title、
keySellingPoint、equipment,根据现实的情况来说因为先有单价才有总房价，
而进行预测的正是单价，所以用不到price、downPayment。观察房屋详情，发现
其中的数据有错误，有的20多层的楼房却显示没有电梯，这不符合高层住房电梯
规定，7层及以上住房必须安装电梯，不符合实际，所有房产有无电梯根据总楼层数判断
'''
import pandas as pd
import re
import time


def getSizeType(df):
    def findNumber(reStr, sourceStr):
        result_list = re.findall(reStr, sourceStr)
        if len(result_list):
            return result_list[0]
        else:
            return 0

    sizeType_list = []
    for i in range(len(df)):
        sizeType = df['sizeType'].iloc[i]
        sizeType_dict = dict(
            room=findNumber('([0-9]*)室', sizeType),
            hall=findNumber('([0-9]*)厅', sizeType),
            restroom=findNumber('([0-9]*)卫', sizeType)
        )
        sizeType_list.append(sizeType_dict)
    return pd.DataFrame(sizeType_list, columns=sizeType_list[0].keys())


def getSize(df):
    df1 = df['size'].copy()
    for i in range(len(df)):
        size = float(df['size'].iloc[i].strip("平米"))
        if size < 50:
            df1.iloc[i] = 'size1'
        elif size < 100:
            df1.iloc[i] = 'size2'
        elif size < 150:
            df1.iloc[i] = 'size3'
        elif size < 200:
            df1.iloc[i] = 'size4'
        else:
            df1.iloc[i] = 'size5'
    return pd.get_dummies(df1)


def getUnitPrice(df):
    df1 = df['unitPrice'].copy()
    for i in range(len(df)):
        df1.iloc[i] = df['unitPrice'].iloc[i].strip("元/平米")
    return df1


def getOrientation(df):
    return pd.get_dummies(df['orientation'])


def getHeight(df):
    df1 = df['floor'].copy()
    for i in range(len(df)):
        df1.iloc[i] = df['floor'].iloc[i].split(' ')[0][0]
    return pd.get_dummies(df1)


def getElevator(df):
    ele_list = []
    for i in range(len(df)):
        str1 = df['floor'].iloc[i].split(' ')[1]
        allFloor = int(re.findall("共(.*)层", str1)[0])
        elevator = 1 if allFloor >= 8 else 0
        ele_dict = {'elevator': elevator}
        ele_list.append(ele_dict)
    df1 = pd.DataFrame(ele_list)
    return df1


def getDecoration(df):
    df1 = df['decoration'].copy()
    for i in range(len(df)):
        df1.iloc[i] = df['decoration'].iloc[i].strip('修')
    return pd.get_dummies(df1)


def getCommunity(df):
    df1 = df['community'].copy()
    for i in range(len(df)):
        df1.iloc[i] = 1 if df['community'].iloc[i] == \
                           df['community'].iloc[i] else 0
    return df1


def getDistrict(df):
    df1 = df['region'].copy()
    for i in range(len(df)):
        df1.iloc[i] = df['region'].iloc[i].split('-')[0]
    return pd.get_dummies(df1)


def getRegion(df):
    df1 = df['region'].copy()
    for i in range(len(df)):
        region = df['region'].iloc[i].split('-')[1]
        df1.iloc[i] = region.strip('(').strip(')')
    return pd.get_dummies(df1)


def getSchool(df):
    df1 = df['school'].copy()
    for i in range(len(df)):
        df1.iloc[i] = 1 if df['region'].iloc[i] == \
                           df['region'].iloc[i] else 0
    return df1


def cleanFloor(df):
    for i in range(len(df)):
        if '共' not in df['floor'].loc[i]:
            df = df.drop([i])
    df = df.reset_index(drop=True)
    return df


def cleanSizeType(df):
    for i in range(len(df)):
        if '室' not in df['sizeType'].loc[i]:
            df = df.drop([i])
    df = df.reset_index(drop=True)
    return df


def cleanCommunity(df):
    df = df[df['community'] == df['community']]
    df = df.reset_index(drop=True)
    return df


if __name__ == "__main__":
    startTime = time.time()
    df = pd.read_excel("demoData.xlsx")
    df = cleanCommunity(df)
    df = cleanFloor(df)
    df = cleanSizeType(df)
    # 下面几个字段是列数较少的字段
    unitPrice = getUnitPrice(df)
    sizeType = getSizeType(df)
    elevator = getElevator(df)
    community = getCommunity(df)
    school = getSchool(df)
    # 下面的字段是通过get_dummies方法产生的9-1矩阵，列数较多
    orientaion = getOrientation(df)
    height = getHeight(df)
    size = getSize(df)
    decoration = getDecoration(df)
    district = getDistrict(df)
    region = getRegion(df)

    df_new = pd.concat([unitPrice, sizeType, elevator, community, school, \
                        orientaion, height, size, decoration, district, region], \
                       axis=1)

    df_new.to_excel("数据处理结果.xlsx", columns=df_new.iloc[0].keys())
    print("数据处理共花费%.2f秒" % (time.time() - startTime))
