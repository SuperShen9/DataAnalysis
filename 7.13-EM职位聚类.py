# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from build.Func import gb, or_path

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取数据
file = 'E:\BaiduYunDownload\weixin\K-Means\数据分析岗位.xlsx'
data = pd.read_excel(file)

# 提取训练数据
features = ['薪水', '经验要求', '学历要求', '行业', '融资', '人数']
train_features = data[features]

train_features['薪水'] = train_features['薪水'].apply(lambda x: x.split('k-')[0])

# 转化数值类型
from sklearn import preprocessing

dvec = preprocessing.LabelEncoder()
for col in features[1:]:
    train_features[col] = dvec.fit_transform(train_features[col])

# 规范化到 [0,1] 空间
min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_features)

# 转化二维表格
df = pd.DataFrame(train_x, columns=features)

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# 用来正常显示中文标签
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
mpl.rcParams['axes.unicode_minus'] = False

corr = df[features].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr)
plt.show()

print(df.head())
print('-' * 50)

# 类别总数
no = 50

# EM 算法 - 高斯聚类
from sklearn.mixture import GaussianMixture

# 构造高斯模型
gmm = GaussianMixture(n_components=no, covariance_type='full')
gmm.fit(train_x)

# 训练数据
predict_x = gmm.predict(train_x)

# 训练结果插入原始数据
result = pd.concat((pd.DataFrame(predict_x), data), axis=1)
result.rename(columns={0: u'EM聚类'}, inplace=True)

# -------------------------------------------------------------------

# k-Means 算法
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=no)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)

# 合并聚类结果，插入到原数据中
result = pd.concat((pd.DataFrame(predict_y), result), axis=1)
result.rename(columns={0: u'K-Means聚类'}, inplace=True)

# 结果查看
print(result.head())
print('-' * 50)

# 输出到桌面
result.to_excel(or_path('聚类结果'))
