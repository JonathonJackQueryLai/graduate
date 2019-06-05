#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/9 16:17
# @Author  : @乌鸦坐飞机
# Description   :

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:38:18 2018

@author: aoanng
"""
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier

##创建100个类共10000个样本，每个样本10个特征
X, y = make_blobs(n_samples=10000, n_features=10, centers=100,random_state=0)

## 决策树
clf1 = DecisionTreeClassifier(max_depth=None, min_samples_split=2,random_state=0)
scores1 = cross_val_score(clf1, X, y)
print(scores1.mean())

## 随机森林
clf2 = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=0)
scores2 = cross_val_score(clf2, X, y)
print(scores2.mean())

## ExtraTree分类器集合
clf3 = ExtraTreesClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=0)
scores3 = cross_val_score(clf3, X, y)
print(scores3.mean())