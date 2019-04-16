# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


# 做分类Decision Tree Classifier

def DTC():
    # 准备数据集
    from sklearn.datasets import load_iris

    iris = load_iris()

    # 获取特征集和分类标识
    features = iris.data
    labels = iris.target
    # 查看各特征属性
    # features=pd.DataFrame(features)
    # pd.scatter_matrix(features)
    # plt.show()
    # exit()

    # 随机抽取 30% 的数据作为测试集，其余为训练集
    from sklearn.model_selection import train_test_split

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.3,
                                                                                random_state=0)
    # 创建 CART 分类树
    from sklearn.tree import DecisionTreeClassifier

    clf = DecisionTreeClassifier()

    # 拟合构造 CART 分类树
    clf = clf.fit(train_features, train_labels)
    # 用 CART 分类树做预测
    test_predict = clf.predict(test_features)

    # print(pd.DataFrame([test_labels,test_predict]).T)
    # exit()

    # 预测结果与测试集结果作比对
    from sklearn.metrics import accuracy_score

    score = accuracy_score(test_labels, test_predict)
    print("CART 分类树准确率 %.4lf" % score)


# 做预测 Decision Tree Regressor

def DTR():
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import load_boston
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    from sklearn.tree import DecisionTreeRegressor

    # 准备数据集
    boston = load_boston()

    # 获取特征集和房价
    features = boston.data
    prices = boston.target
    # print(features)
    # print('-'*50)
    # print(prices)
    # exit()

    # 随机抽取 30% 的数据作为测试集，其余为训练集
    train_features, test_features, train_price, test_price = train_test_split(features, prices, test_size=0.3
                                                                              , random_state=2)

    # 创建 CART 回归树
    dtr = DecisionTreeRegressor()
    # 拟合构造 CART 回归树
    dtr.fit(train_features, train_price)
    # 预测测试集中的房价
    predict_price = dtr.predict(test_features)
    # 测试集的结果评价
    print('回归树二乘偏差均值:', mean_squared_error(test_price, predict_price))
    print('回归树绝对值偏差均值:', mean_absolute_error(test_price, predict_price))
