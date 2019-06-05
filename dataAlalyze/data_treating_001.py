#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 11:10
# @Author  : @乌鸦坐飞机
# Description   :
import pandas as pd
import numpy as np

housing_data = pd.read_csv('..\crawl\SFUN\SFUN.csv')

pd.DataFrame(housing_data)
# # 分析数据集
# from sklearn import datasets
#
# #  sklearn自带的datasets中就有Boston房价数据集
# dataset_X = housing_data._data
# # print('X:',dataset_X)
# # 获取影响房价的特征向量，作为feaure
# dataset_y = housing_data.
# # print('Y:',dataset_y)
# #  获取对应的房价，作为label y
# # print(dataset_X.shape)
# # (506, 13)
# #  一共有506个样本，每个样本有13个features
#
# print(dataset_y.shape)  # (506,)
# print(dataset_X[:5, :])
#
# # 打印看看features的数值类型和大小，貌似已经normalize.
# #  将整个数据集划分为train set 和test set两部分
# from sklearn.utils import shuffle
#
# dataset_X, dataset_y = shuffle(dataset_X, dataset_y)
# print(dataset_X[:5, :])
# # 确认dataset_X 的确发生了 shuffle
#
# num_split = int(0.8 * len(dataset_X))
# train_X, train_y = dataset_X[:num_split], dataset_y[:num_split]
# test_X, test_y = dataset_X[num_split:], dataset_y[num_split:]
# print(train_X.shape)  # (404, 13)
# print(test_X.shape)
# # (102, 13)# 上面的数据集划分也可以采用下面的方法：
# from sklearn.model_selection import train_test_split
#
# dataset_y = dataset_y[:, np.newaxis]
# dataset = np.hstack((dataset_X, dataset_y))
# # print(dataset.shape)
# print(dataset[:, :3])
# train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=37)
# print(train_set.shape)
# # (404, 14)
# print(test_set.shape)
# # (102, 14)
#
#
# # 构建决策树回归模型
# from sklearn.tree import DecisionTreeRegressor
#
# decision_regressor = DecisionTreeRegressor(max_depth=4)
# # 最大深度确定为4
# decision_regressor.fit(train_X, train_y)
# #  对决策树回归模型进行训练# 使用测试集来评价该决策树回归模型
# predict_test_y = decision_regressor.predict(test_X)
# import sklearn.metrics as metrics
#
# # print('决策树回归模型的评测结果----->>>')
# print('均方误差MSE：{}'.format(
#     round(metrics.mean_squared_error(predict_test_y, test_y), 2)))
# print('解释方差分：{}'.format(
#     round(metrics.explained_variance_score(predict_test_y, test_y), 2)))