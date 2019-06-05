#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 10:59
# @Author  : @乌鸦坐飞机
# Description   :  特征选择
from sklearn import metrics
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils import shuffle

df = pd.read_csv('myClean2.csv')

# print(df)
def pca_down_feature(t_df):
    # t_df = pd.read_csv('myClean1.csv')
    first_array = []
    for i in range(len(t_df)):
        sample = list(t_df.iloc[i])[2:]
        first_array.append(sample)
    dataset_X = np.array(first_array)
    dataset_y = np.array(t_df['perPrice'])
    dataset_X, dataset_y = shuffle(dataset_X, dataset_y)
    pca = PCA(n_components=11)
    pca.fit(dataset_X)
    x = pca.transform(dataset_X)
    # print(pca.explained_variance_ratio_.tolist())
    dataset_X = x
    return (dataset_X,dataset_y)
dataset_X = pca_down_feature(df)[0]
dataset_y = pca_down_feature(df)[1]

num_split = int(0.8 * len(dataset_X))
train_X, train_y = dataset_X[:num_split], dataset_y[:num_split]
test_X, test_y = dataset_X[num_split:], dataset_y[num_split:]
for i in range(4,11):
    print(i)
    decision_regressor = DecisionTreeRegressor(criterion='mse', max_depth=i)
    # 训练模型
    decision_regressor.fit(train_X, train_y)
    predict_test_y = decision_regressor.predict(test_X)
    print('决策树深度为i解释方差分：{0}'.format(
        round(metrics.explained_variance_score(test_y, predict_test_y), 2)))