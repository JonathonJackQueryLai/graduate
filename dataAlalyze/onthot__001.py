#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 19:29
# @Author  : @乌鸦坐飞机
# Description   :
import pandas as pd

df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'], 'data': range(6)})
dummies = pd.get_dummies(df['key'],prefix='key')
new_df = df[['data']].join(dummies)
print('df:',df)
print('new_df',new_df)