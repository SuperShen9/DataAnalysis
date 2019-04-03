# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

# 用来正常显示中文标签
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']

import warnings

warnings.filterwarnings('ignore')

# 导入线性回归模块
from sklearn.linear_model import LinearRegression


def LR1():
    # 固定随机种子
    rdm = np.random.RandomState(3)

    # 生成随机数x,y
    xtrain = 10 * rdm.rand(30)
    ytrain = 3 + 2 * xtrain + rdm.rand(30)

    model = LinearRegression()
    model.fit(xtrain[:, np.newaxis], ytrain)

    xtest = np.linspace(0, 10, 1000)
    ytest = model.predict(xtest[:, np.newaxis])

    # 样本作图
    fig = plt.figure(figsize=(12, 3))
    fig.add_subplot(1, 2, 1)
    plt.scatter(xtrain, ytrain, marker='.', color='k')
    plt.grid()
    plt.title('样本数据散点图')

    # 线性回归作图
    fig.add_subplot(1, 2, 2)
    plt.scatter(xtrain, ytrain, marker='.', color='k')
    plt.plot(xtest, ytest, color='r')
    plt.grid()
    plt.title('线性回归拟合')

    print('斜率a为：%.4f,' % model.coef_[0], '截距b为：%.4f' % model.intercept_)
    print('线性回归函数为： y = %.0fx + %.2f' % (model.coef_[0], model.intercept_))

    plt.show()


def LRM():
    # 多元线性回归
    rdm = np.random.RandomState(1)
    xtrain = 10 * rdm.rand(150, 4)
    ytrain = 20 + np.dot(xtrain, [1.5, 2, -4, 3])
    # 创建数据，其中包括4个相互独立自变量
    df = pd.DataFrame(xtrain, columns=['b1', 'b2', 'b3', 'b4'])
    df['y'] = ytrain

    pd.scatter_matrix(df[['b1', 'b2', 'b3', 'b4']], figsize=(10, 6),
                      diagonal='kde',
                      alpha=0.5,
                      range_padding=0.1)

    # 多元回归拟合
    model = LinearRegression()
    model.fit(df[['b1', 'b2', 'b3', 'b4']], df['y'])

    # 参数输出
    print('斜率a为：', model.coef_)
    print('截距b为：%.4f' % model.intercept_)
    print('线性回归函数为：\ny = %.1fx1 + %.1fx2 + %.1fx3 + %.1fx4 + %.1f'
          % (model.coef_[0], model.coef_[1], model.coef_[2], model.coef_[3], model.intercept_))

    plt.show()

# 模型评估
from sklearn import metrics

# 创建数据
rdm = np.random.RandomState(2)
xtrain = 10 * rdm.rand(30)
ytrain = 8 + 4 * xtrain + rdm.rand(30) * 3

# 多元回归拟合
model = LinearRegression()
model.fit(xtrain[:, np.newaxis], ytrain)

# 求出预测数据
ytest = model.predict(xtrain[:, np.newaxis])

# 求出均方差
mse = metrics.mean_squared_error(ytrain, ytest)

# 求出均方根
rmse = np.sqrt(mse)

# 求出预测数据与原始数据均值之差的平方和
ssr = ((ytest - ytrain.mean()) ** 2).sum()

# 求出原始数据和均值之差的平方和
sst = ((ytrain - ytrain.mean()) ** 2).sum()

# 求出确定系数
r2 = ssr / sst

# 求出确定系数
r2 = model.score(xtrain[:, np.newaxis], ytrain)
print("均方差MSE为: %.5f" % mse)
print("均方根RMSE为: %.5f" % rmse)
print("确定系数R-square为: %.5f" % r2)
