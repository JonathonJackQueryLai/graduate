#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 21:31
# @Author  : @乌鸦坐飞机
# Description   :
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 回归决策树解决预测房价问题
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeRegressor
# 分析数据
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score

df = pd.read_csv('myClean3.csv')
first_array = []
for i in range(len(df)):
    sample = list(df.iloc[i])[2:]
    first_array.append(sample)
dataset_X = np.array(first_array)
dataset_y = np.array(df['perPrice'])
# print(dataset_X.shape)
# print(dataset_y.shape)  # (506,)

dataset_X, dataset_y = shuffle(dataset_X, dataset_y)  # 打乱 增加模型的鲁棒性
# # 确认dataset_X 的确发生了 shuffle
# 五分法
num_split = int(0.8 * len(dataset_X))
train_X, train_y = dataset_X[:num_split], dataset_y[:num_split]
test_X, test_y = dataset_X[num_split:], dataset_y[num_split:]

# print(train_X.shape)  # (404, 13)
# print(test_X.shape)
# # (102, 13)# 上面的数据集划分也可以采用下面的方法：
# from sklearn.model_selection import train_test_split
#
# dataset_y = dataset_y[:, np.newaxis]
# dataset = np.hstack((dataset_X, dataset_y))
# # # print(dataset.shape)
# # print(dataset[:, :3])
# train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=37)

# # 构建决策树回归模型

# 自己做比较
# for i in range(10):
#     print('第%d次:\n' % i)
#     # 预测值
#     for i in range(8, 10):
#         # 创建实例
#         decision_regressor = DecisionTreeRegressor(criterion='mse', max_depth=i)
#         # 训练模型
#         decision_regressor.fit(train_X, train_y)
#         predict_test_y = decision_regressor.predict(test_X)
#         print('决策树深度为{1}解释方差分：{0}'.format(
#             round(metrics.explained_variance_score(test_y, predict_test_y), 2), i))

# decision_regressor = DecisionTreeRegressor(criterion='mse', max_depth=8)
# # 训练模型
# decision_regressor.fit(train_X, train_y)
# predict_test_y = decision_regressor.predict(test_X)
# print('决策树深度8的解释方差分：{0}'.format(
#     round(metrics.explained_variance_score(test_y, predict_test_y), 2)))

# 线性回归
# regr = linear_model.LinearRegression(fit_intercept=True, normalize=False,
#     copy_X=True, n_jobs=1)
# regr.fit(train_X, train_y)
# res_LIN = regr.predict(test_X)
# print('线性回归解释方差分：{}'.format(
#     round(metrics.explained_variance_score(test_y, res_LIN), 2)))


# 随机森林
from sklearn.ensemble import RandomForestRegressor

RFR = RandomForestRegressor(n_estimators=15, max_depth=11, min_samples_split=2, random_state=10, bootstrap=True,criterion='mse')
RFR.fit(train_X, train_y)
res_RFR = RFR.predict(test_X)
aa = format(round(metrics.explained_variance_score(test_y, res_RFR), 2))
# bb = metrics.accuracy_score(test_y, res_RFR)  只能用于分类问题

print(aa)
if float(aa) >= 0.68:
    joblib.dump(RFR, 'regr_model.pickle')
# print('随机森林解释方差分：{}'.format(
#     round(metrics.explained_variance_score(test_y, res_RFR), 2)))
# 保存模型
# joblib.dump(RFR, 'RFR_model.pickle')
# joblib.dump(regr, 'regr_model.pickle')
# joblib.dump(decision_regressor, 'dr_model.pickle')
# print('accury:', res_RFR.oob_score_)
