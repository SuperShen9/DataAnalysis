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

# print(train_features.head())
# print(train_features.info())
# exit()

# 转化数值类型
from sklearn import preprocessing
dvec = preprocessing.LabelEncoder()
for col in features[1:]:
    train_features[col] = dvec.fit_transform(train_features[col])

# 规范化到 [0,1] 空间
min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_features)

# print(train_features)
# exit()

# k-Means 算法
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)

# 合并聚类结果，插入到原数据中
result = pd.concat((pd.DataFrame(predict_y), data), axis=1)
result.rename(columns={0: u'聚类'}, inplace=True)

result.to_excel(or_path('聚类结果'))
# print(result)
# exit()

# 输出聚类效果
df = pd.DataFrame(result.groupby('聚类').apply(lambda x: list(x['公司'] + '-' + x['职位'])))
df.to_excel(or_path('职位分类'))
print(df)