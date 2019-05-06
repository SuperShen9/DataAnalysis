# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

import warnings

warnings.filterwarnings('ignore')

from sklearn import preprocessing
import numpy as np

# 初始化数据，每一行表示一个样本，每一列表示一个特征
x = np.array([[0., -3., 1.],
              [3., 1., 2.],
              [0., 1., -1.]])

def Normailize(x):

    # 将数据进行 [0,1] 规范化（min_max规范化）
    min_max_scaler = preprocessing.MinMaxScaler()
    minmax_x = min_max_scaler.fit_transform(x)
    print(minmax_x)
    print('-' * 50)

    # 将数据进行 Z-Score 规范化
    scaled_x = preprocessing.scale(x)
    print(scaled_x)
    print('-' * 50)

    from sklearn.preprocessing import StandardScaler
    ss = StandardScaler()
    scaled_x2 = ss.fit_transform(x)
    print(scaled_x2)
    print('-' * 50)


    # 小数定标规范化
    j = np.ceil(np.log10(np.max(abs(x))))
    scaled_y = x / (10 ** j)

    print(scaled_y)

Normailize(x)