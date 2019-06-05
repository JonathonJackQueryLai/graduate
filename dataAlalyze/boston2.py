#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/7 17:10
# @Author  : @乌鸦坐飞机
# Description   :


from sklearn.model_selection import  train_test_split
from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import mean_squared_error,mean_absolute_error

'''注：回归树的叶节点的数据类型不是离散型，而是连续型，决策树每个叶节点依照训练数据表现的概率倾向决定最终的预测类别，而回归树叶节点是连续的，节点的值是‘一团数据’的均值'''

#导入数据
boston = load_boston()
#查看数据信息print(boston.DESCR)
X = boston.data
y = boston.target
#对数据进行分割
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=33)
ss_X = StandardScaler()
# ss_y =StandardScaler()
#分别对训练和测试数据的特征及目标值进行标准化处理
X_train = ss_X.fit_transform(X_train)
X_test = ss_X.transform(X_test)
y_train = ss_X.fit_transform(y_train)
y_test = ss_X.transform(y_test)
#使用默认的配置初始化DecisionTreeRegressor
dtr = DecisionTreeRegressor()
#用波士顿房价的数据构建回归树
dtr.fit(X_train,y_train)
#使用默认配置的单一回归树对测试数据进行测试
dtr_y_predict = dtr.predict(X_test)

#使用R-squared,MSE以及MAE三种指标对默认配置的回归树在测试集上进行性能评估
print('R-squared value of DecisionTreeRegressor:',dtr.score(X_test,y_test))
print('\n'*2)
print('The mean squared error of DecisionTreeRegressor: ',mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(dtr_y_predict)))
print('\n'*2)

print('The mean absolute error of DecisionTreeRegressor:',mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(dtr_y_predict)))
