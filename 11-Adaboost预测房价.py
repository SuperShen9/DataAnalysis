# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import matplotlib.pyplot as plt
from build.Func import or_path

# 防错提醒
import warnings

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_boston
from sklearn.ensemble import AdaBoostRegressor

# 加载数据
data = load_boston()

# 查看数据
# df = pd.DataFrame(data.data, columns=data.feature_names)
# df['price'] = data.target
# print(df.head())
# exit()

# 分割数据
train_x, test_x, train_y, test_y = train_test_split(data.data,
          data.target, test_size=0.25, random_state=33)

# 使用 AdaBoost 回归模型
regressor = AdaBoostRegressor()
regressor.fit(train_x, train_y)
pred_y = regressor.predict(test_x)

mse = mean_squared_error(test_y, pred_y)
print("Adaboost 均方误差 = ", round(mse, 2))

# 将结果输出来
df = pd.DataFrame(test_x, columns=data.feature_names)
df['price'] = test_y
df['price_ada'] = pred_y

# 使用决策树回归模型
from sklearn.tree import DecisionTreeRegressor

dec_regressor = DecisionTreeRegressor()
dec_regressor.fit(train_x, train_y)
pred_y = dec_regressor.predict(test_x)

mse = mean_squared_error(test_y, pred_y)
print("决策树 均方误差 = ", round(mse, 2))

# 存放到df
df['price_tree'] = pred_y

# 使用 KNN 回归模型
from sklearn.neighbors import KNeighborsRegressor

knn_regressor = KNeighborsRegressor()
knn_regressor.fit(train_x, train_y)
pred_y = knn_regressor.predict(test_x)

mse = mean_squared_error(test_y, pred_y)
print("KNN 均方误差 = ", round(mse, 2))

# 存放到df
df['price_KNN'] = pred_y

# 使用SVM 回归模型
from sklearn import svm

model = svm.SVR()
model.fit(train_x, train_y)
pred_y = model.predict(test_x)

mse = mean_squared_error(test_y, pred_y)
print("SVM 均方误差 = ", round(mse, 2))

# 存放到df
df['price_SVM'] = pred_y

# 将数据放到桌面
df.to_excel(or_path('各模型回归预测'))

# 画图
df = pd.read_excel(or_path('各模型回归预测'))
print(df.head())

for col in df.columns[-4:]:
    fig = plt.figure(figsize=(13, 7))
    df['price'].plot(color='black')
    df[col].plot(color='lime', linestyle='-.')
    plt.legend(loc='upper right')
    plt.savefig('C:\\Users\Administrator\Desktop\\{}'.format(col))
