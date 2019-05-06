# -*- coding: utf-8 -*-
# author：Super

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

import warnings

warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_csv('E:\BaiduYunDownload\weixin\credit\data.csv')

# # 数据探索
print(df.head())
print(df.info())

# 查看下个月违约率
print(df.groupby('payment_next_month').size())

# 删除无效列
df.drop('ID', axis=1, inplace=True)

features = df[df.columns[:-1]]
target = df[df.columns[-1:]]

# 30% 作为测试集，其余作为训练集
from sklearn.model_selection import train_test_split

train_x, test_x, train_y, test_y = train_test_split(features,
                                                    target, test_size=0.30, stratify=target, random_state=1)

# 构建随机森林模型
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()

# 拟合数据
rf.fit(train_x, train_y)

# 预测结果
predict_y = rf.predict(test_x)
print(predict_y)

# 预测结果与测试集结果作比对
from sklearn.metrics import accuracy_score

score = accuracy_score(test_y, predict_y)
print("\n随机森林 分类准确率 %.4lf" % score)
