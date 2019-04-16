# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

import warnings
warnings.filterwarnings('ignore')

# ----------------数据读取-------------------------------
file_path = 'E:\BaiduYunDownload\weixin\Titanic_Data\\'
train_data = pd.read_csv(file_path + 'train.csv')
test_data = pd.read_csv(file_path + 'test.csv')

# 信息查看
# print(train_data.info())
# print('-' * 80)
# print(train_data.describe())
# print('-' * 80)
# print(train_data.head())

# ------------------数据清洗-------------------------------------------

# 使用平均年龄来填充年龄中的 nan 值
train_data['Age'].fillna(train_data['Age'].mean(), inplace=True)
test_data['Age'].fillna(test_data['Age'].mean(), inplace=True)

# 使用票价的均值填充票价中的 nan 值
train_data['Fare'].fillna(train_data['Fare'].mean(), inplace=True)
test_data['Fare'].fillna(test_data['Fare'].mean(), inplace=True)

# 查看信息
# print(train_data.info())
# print(train_data.groupby('Embarked').size())

# 使用登录最多的港口来填充登录港口的 nan 值
train_data['Embarked'].fillna('S', inplace=True)
test_data['Embarked'].fillna('S', inplace=True)

# 查看信息
# print(train_data.info())

# -------------------------特征选择----------------------------------------
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
train_features = train_data[features]
train_labels = train_data['Survived']
test_features = test_data[features]

# ------------------------转化数值类型-------------------------------------
from sklearn.feature_extraction import DictVectorizer

dvec = DictVectorizer(sparse=False)
train_features = dvec.fit_transform(train_features.to_dict(orient='record'))

# # ------------------------转化数值类型2-------------------------------------
# from sklearn import preprocessing
# dvec = preprocessing.LabelEncoder()
# train_features['Sex'] = dvec.fit_transform(train_features['Sex'])
# train_features['Embarked'] = dvec.fit_transform(train_features['Embarked'])
# print(train_features.sample(10))
# exit()


# 查看结果
# print(pd.DataFrame(train_features,columns=dvec.feature_names_))

# 构造 ID3 决策树, 默认是基尼系数
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(criterion='entropy')

# 决策树训练
clf.fit(train_features, train_labels)

# 测试数据类型转换
test_features = dvec.transform(test_features.to_dict(orient='record'))

# 决策树预测
test_labels = clf.predict(test_features)

# 打印最终结果
# print(test_labels)

# 输出到csv文件
test_data['Survive'] = test_labels
# print(test_data.head(5))

# 得到决策树准确率
acc_decision_tree = round(clf.score(train_features, train_labels), 6)
print('\nscore 准确率为 %.4lf' % acc_decision_tree)

import numpy as np
from sklearn.model_selection import cross_val_score
# 使用 K 折交叉验证 统计决策树准确率
print('\ncross_val_score 准确率为 %.4lf' % np.mean(cross_val_score(clf, train_features, train_labels, cv=10)))
