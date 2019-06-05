#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : pandas
import matplotlib.pyplot as PLT
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


# 回归决策树 一个demo 例子
# 拟合效果不好
def creat_data(n):
    np.random.seed(0)
    X = 5 * np.random.rand(n, 1)
    Y = np.sin(X).ravel()
    noise_num = (int)(n / 5)
    Y[::5] += 3 * (0.5 - np.random.rand(noise_num))
    return train_test_split(X, Y, test_size=0.25, random_state=1)


def test_DescisonTreeRe(*data):
    X_train, X_test, Y_train, Y_test = data
    regr = DecisionTreeRegressor()
    regr.fit(X_train, Y_train)
    print("Training code:%f" % (regr.score(X_train, Y_train)))
    print("Testing code:%f" % (regr.score(X_test, Y_test)))

    ## 绘图
    fig = PLT.figure()
    ax = fig.add_subplot(1, 1, 1)
    X = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    Y = regr.predict(X)
    ax.scatter(X_train, Y_train, label="train sample", c='g')
    ax.scatter(X_test, Y_test, label="test sample", c='r')
    ax.plot(X, Y, label='predict_value', lw=2, alpha=0.5)
    ax.set_xlabel('data')
    ax.set_title("Decision_tree")
    ax.legend(framealpha=0.5)
    PLT.show()


def test_splitter(*data):
    X_train, X_test, Y_train, Y_test = data
    splitters = ['best', 'random']
    for splitter in splitters:
        regr = DecisionTreeRegressor(splitter=splitter)
        regr.fit(X_train, Y_train)
        print("splitter %s" % splitter)
        print('training score:%f' % (regr.score(X_train, Y_train)))
        print('testing score%f' % (regr.score(X_test, Y_test)))


def test_depth(*data, maxdepth):
    X_train, X_test, Y_train, Y_test = data
    depths = np.arange(1, maxdepth)
    train_scores = []
    test_scores = []

    for depth in depths:
        regr = DecisionTreeRegressor(max_depth=depth)
        regr.fit(X_train, Y_train)
        train_scores.append(regr.score(X_train, Y_train))
        test_scores.append(regr.score(X_test, Y_test))

    # 绘图
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(depths, train_scores, label='training score')
    ax.plot(depths, test_scores, label="test score")
    ax.set_xlabel('maxdepth')
    ax.set_ylabel('score')
    ax.set_title('DTR')
    ax.legend(framealpha=0.5)
    plt.show()


X_Train, X_test, y_train, y_test = creat_data(100)
test_depth(X_Train, X_test, y_train, y_test, maxdepth=3)
