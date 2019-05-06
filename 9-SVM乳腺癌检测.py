# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

import matplotlib.pyplot as plt
import seaborn as sns

# 防错提醒
import warnings

warnings.filterwarnings('ignore')

# 加载数据集，你需要把数据放到目录中
data = pd.read_csv('E:\BaiduYunDownload\weixin\\Breast_cancer_data\\data.csv')

# 将特征字段分成 3 组
features_mean = list(data.columns[2:12])
features_se = list(data.columns[12:22])
features_worst = list(data.columns[22:32])

# ----------------数据清洗---------------------------------

# ID 列没有用，删除该列
data.drop("id", axis=1, inplace=True)
data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

# 将肿瘤诊断结果可视化
sns.countplot(data['diagnosis'], label="Count")
plt.show()

# 用热力图呈现 features_mean 字段之间的相关性
corr = data[features_mean].corr()
plt.figure(figsize=(12, 12))
sns.heatmap(corr)
plt.show()

# 特征选择
features_remain = ['radius_mean', 'texture_mean', 'smoothness_mean',
                   'compactness_mean', 'symmetry_mean', 'fractal_dimension_mean']

# 抽取 30% 的数据作为测试集，其余作为训练集
from sklearn.model_selection import train_test_split

train, test = train_test_split(data, test_size=0.3)

print('\n总数据量：{}'.format(data.shape[0]))
print('训练集数据量：{}'.format(train.shape[0]))
print('测试集数据量：{}'.format(test.shape[0]))

# 抽取特征选择的数值作为训练和测试数据
train_X = train[features_remain]
train_y = train['diagnosis']
test_X = test[features_remain]
test_y = test['diagnosis']

# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)

# 创建 SVM 分类器
from sklearn import svm
model = svm.SVC()
model.fit(train_X, train_y)

# 用测试集做预测
from sklearn import metrics
prediction = model.predict(test_X)
print('\n准确率: ', metrics.accuracy_score(prediction, test_y))

# -----------全部特殊预测 / 过拟合试验----------------------------

# 抽取特征选择的数值作为训练和测试数据
train_X = train
train_y = train['diagnosis']
test_X = test
test_y = test['diagnosis']

# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)

# 创建 SVM 分类器
model = svm.SVC()
# 用训练集做训练
model.fit(train_X, train_y)
# 用测试集做预测
prediction = model.predict(test_X)
print('全部特征准确率: ', metrics.accuracy_score(prediction, test_y))
