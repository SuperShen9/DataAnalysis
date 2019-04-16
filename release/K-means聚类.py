# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


# 输入数据

file = 'E:\BaiduYunDownload\weixin\\20190225\data.csv'

data = pd.read_csv(file, encoding='gbk')

# print(data)
# exit()

train_x = data[data.columns[1:]]

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)

# 规范化到 [0,1] 空间

from sklearn import preprocessing

min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_x)

# print(train_x)
# exit()

# kmeans 算法

kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)


# 合并聚类结果，插入到原数据中

result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
result.rename(columns={0: u'聚类'}, inplace=True)

print(result)
# exit()


print(result.groupby('聚类').apply(lambda x: list(x['国家'])))
