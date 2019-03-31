# -*- coding: utf-8 -*-
# author：Super

from build.Func import or_path
import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

# 数据加载，避免中文乱码问题
file = 'E:\BaiduYunDownload\weixin\\20190301\\heros.csv'
df = pd.read_csv(file, encoding='gb18030')
features = df.columns[1:-2]
data = df[features]

# 对英雄属性之间的关系进行可视化分析

# # 设置 plt 正确显示中文
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# # 用热力图呈现 features_mean 字段之间的相关性
# corr = data[features].corr()
# plt.figure(figsize=(14, 14))
# sns.heatmap(corr, annot=True)
# plt.show()
# exit()

# 相关性大的属性保留一个，因此可以对属性进行降维
features_remain = [u'最大生命', u'初始生命', u'最大法力', u'最高物攻',
                   u'初始物攻', u'最大物防', u'初始物防', u'最大每5秒回血',
                   u'最大每5秒回蓝', u'初始每5秒回蓝', u'最大攻速', u'攻击范围']

data = df[features_remain]
data[u'最大攻速'] = data[u'最大攻速'].apply(lambda x: float(x.strip('%')) / 100)
data[u'攻击范围'] = data[u'攻击范围'].map({'远程': 1, '近战': 0})



# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
data = ss.fit_transform(data)

# 构造 GMM 聚类
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=30, covariance_type='full')
gmm.fit(data)

# 训练数据
prediction = gmm.predict(data)
# print(prediction)
# exit()

# 将分组结果输出到 CSV 文件中

df.insert(0, '分组', prediction)
df.sort_values('分组', ascending=1, inplace=True)
df.to_excel(or_path('英雄分类结果'), index=False)

print(df.groupby('分组').apply(lambda x: list(x['英雄'])))
