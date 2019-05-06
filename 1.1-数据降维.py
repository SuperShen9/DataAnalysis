# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import matplotlib.pyplot as plt
from build.Func import or_path

import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据集，你需要把数据放到目录中
data = pd.read_csv('E:\BaiduYunDownload\weixin\\Breast_cancer_data\\data.csv')
features = list(data.columns[2:])

print(data.head())

# ID 列没有用，删除该列
data.drop("id", axis=1, inplace=True)
data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

print(data.head())

# 抽取 30% 的数据作为测试集，其余作为训练集
from sklearn.model_selection import train_test_split
train, test = train_test_split(data, test_size=0.3)

print('\n总数据量：{}'.format(data.shape[0]))
print('训练集数据量：{}'.format(train.shape[0]))
print('测试集数据量：{}\n'.format(test.shape[0]))

# 抽取特征选择的数值作为训练和测试数据
train_X = train[features]
train_y = train['diagnosis']
test_X = test[features]
test_y = test['diagnosis']

# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.transform(test_X)

# 用热力图呈现特征之间的相关性
corr = data[features].corr()
print(type(corr))
plt.figure(figsize=(14, 14))
sns.heatmap(corr)
plt.show()

#------------- 构建降维模型----------------------
from sklearn.decomposition import PCA
pca = PCA(n_components=6)

# 数据模型转化
train_X = pca.fit_transform(train_X)
test_X = pca.fit_transform(test_X)

print(train_X)

# 创建 SVM 分类器
from sklearn import svm
model = svm.SVC()
model.fit(train_X, train_y)

# 用测试集做预测
from sklearn import metrics
prediction = model.predict(test_X)
print('\n准确率: ', metrics.accuracy_score(prediction, test_y))

