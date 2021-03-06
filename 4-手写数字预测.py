# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

from sklearn.datasets import load_digits

digit = load_digits()
features = digit.data
labels = digit.target

# 数据规范化
from sklearn import preprocessing
features = preprocessing.scale(features)

# 数据展示
# import matplotlib.pyplot as plt
# plt.gray()
# plt.imshow(digit.images[8])
# plt.show()


# 随机抽取 30% 的数据作为测试集，其余为训练集
from sklearn.model_selection import train_test_split

train_features, test_features, train_labels, test_labels \
    = train_test_split(features, labels, test_size=0.3)

# 创建 CART 分类树
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()

# 拟合构造 CART 分类树
clf = clf.fit(train_features, train_labels)

# 用 CART 分类树做预测
test_predict = clf.predict(test_features)

# # 比对原始标签和预测标签
# print(pd.DataFrame([test_labels, test_predict]).T)

# 预测结果与测试集结果作比对
from sklearn.metrics import accuracy_score
score = accuracy_score(test_labels, test_predict)
print("\nCART 分类树准确率 %.4lf" % score)
