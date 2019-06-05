#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 回归决策树解决预测房价问题

import numpy as np
# 分析数据集
from sklearn import datasets

#  sklearn自带的datasets中就有Boston房价数据集
housing_data = datasets.load_boston()
print('housing_data:', housing_data)
# print('housing_data:', type(housing_data))
dataset_X = housing_data.data
# print('X:',dataset_X)
# 获取影响房价的特征向量，作为feaure
dataset_y = housing_data.target

# print('Y:',dataset_y)
#  获取对应的房价，作为label y
# print(dataset_X.shape)
# (506, 13)
#  一共有506个样本，每个样本有13个features

# print(dataset_y.shape)  # (506,)
print(dataset_X[:5, :])

# 打印看看features的数值类型和大小，貌似已经normalize.
#  将整个数据集划分为train set 和test set两部分
from sklearn.utils import shuffle

dataset_X, dataset_y = shuffle(dataset_X, dataset_y)
# print(dataset_X[:5, :])
# 确认dataset_X 的确发生了 shuffle

num_split = int(0.8 * len(dataset_X))
train_X, train_y = dataset_X[:num_split], dataset_y[:num_split]
test_X, test_y = dataset_X[num_split:], dataset_y[num_split:]


# (102, 13)# 上面的数据集划分也可以采用下面的方法：
from sklearn.model_selection import train_test_split

dataset_y = dataset_y[:, np.newaxis]
dataset = np.hstack((dataset_X, dataset_y))
# print(dataset.shape)
print(dataset[:, :3])
train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=37)
# print(train_set.shape)
# # (404, 14)
# print(test_set.shape)
# # (102, 14)


# 构建决策树回归模型
from sklearn.tree import DecisionTreeRegressor

decision_regressor = DecisionTreeRegressor(criterion='mse',max_depth=4)
# 最大深度确定为4
decision_regressor.fit(train_X, train_y)
#  对决策树回归模型进行训练# 使用测试集来评价该决策树回归模型
print('test_X:',test_X)
print('test_X.type()',test_X)
predict_test_y = decision_regressor.predict(test_X)

'''
    在feed data的过程中，我们总是会用到samle_weight,样本权重的直观理解为：样本权重给出了各个样本的重要性。
   具体是怎么体现的了，首先样本权重不是把样本乘以一个系数，这样的话feature值不就改变了，他改变的是该样本的数量，本来一个样本是1个，现在变成了0.8个，或者1.5个，样本数 量现在可以取小数个了，对应的这个样本在总体样本中的占比也会变化。

'''
# 在进行机器学习时，经常需要打乱样本  shuddle
import sklearn.metrics as metrics

print('-----决策树回归模型的评测结果-----')
print('均方误差MSE：{}'.format(
    round(metrics.mean_squared_error(predict_test_y, test_y),2)))
print('解释方差分：{}'.format(
    round(metrics.explained_variance_score(predict_test_y, test_y), 2)))
# # import pickle
#
# # 保存模型
# with open('model.pickle', 'wb') as f:
#     pickle.dump(decision_regressor, f)
#
#
# from sklearn.externals import joblib
#
# # 保存模型
# joblib.dump(decision_regressor, 'model.pickle')
#
# #载入模型
# model = joblib.load('model.pickle')


