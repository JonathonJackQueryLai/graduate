#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 14:19
# @Author  : @乌鸦坐飞机
# Description   :

import joblib
import numpy as np


# import pickle
#
# # 保存模型
# with open('model11.pickle', 'wb') as f:
#     pickle.dump(decision_regressor, f)

# from sklearn.externals import joblib
#
# # 保存模型
# joblib.dump(decision_regressor, 'model.pickle')
# #
# #载入模型
# model = joblib.load('model.pickle')
# 保存模型
# joblib.dump(decision_regressor, 'model.pickle')
#
# 载入模型
x = [3, 2, 2, 3, 1, 0, 2, 1, 2.2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
# d = x.reshape((-1,1))
x = np.array([list(x)])
# x = x.reshape(-1, 1)
model = (joblib.load(r'F:\Users\python\PycharmProjects\webAddress_New\dataAlalyze\model11.pickle'))

result = model.predict(x)
print(result)
