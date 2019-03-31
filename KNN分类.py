# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
from build.Func import or_path
from Func import gb
import warnings

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt


# 加载数据
digits = load_digits()
data = digits.data
# 数据探索
# print(data[:3])
# exit()
# # 查看第一幅图像
# print(digits.images[0])
#
# # 第一幅图像代表的数字含义
# print(digits.target[0])

# # 将第一幅图像显示出来
# plt.gray()
# plt.imshow(digits.images[38])
# plt.show()


# 分割数据，将 25% 的数据作为测试集，其余作为训练集（你也可以指定其他比例的数据作为训练集）
train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.25)

# print(type(train_x), type(test_x))
# exit()

# 采用 Z-Score 规范化
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)
test_ss_x = ss.transform(test_x)


# 创建 KNN 分类器
knn = KNeighborsClassifier()
knn.fit(train_ss_x, train_y)
predict_y = knn.predict(test_ss_x)
print("KNN 准确率: %.4lf" % accuracy_score(predict_y, test_y))






# x = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
#
# train_x, test_x = train_test_split(x, test_size=0.2)
#
# print(train_x)
# print('-' * 20)
# print(test_x)
#
# print('-' * 50)
# # exit()
#
# ss = preprocessing.StandardScaler()
# train_ss_x = ss.fit_transform(train_x)
# test_ss_x = ss.transform(test_x)
#
# print(train_ss_x)
# print('-' * 20)
# print(test_ss_x)
# exit()
