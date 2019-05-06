# -*- coding: utf-8 -*-
# author：Super.Shen
import numpy as np
import pandas as pd
from build.Func import gb, or_path

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取数据
file = 'E:\BaiduYunDownload\weixin\\boss直聘_数据清洗\数据分析岗位.xlsx'
df = pd.read_excel(file)

# 删除无效列
list1 = ['url', 'HR状态', '工作内容', '法人代表', '公司介绍']

for col in list1:
    del df[col]

# print(df.info())

# 清理薪水
df['薪水'] = df['薪水'].apply(lambda x: int(x.split('k-')[0]))

# 清理地区
df['地区'] = df['地区'].apply(lambda x: x.split(' ')[1])

# 清理经验
df['经验要求'] = df['经验要求'].apply(lambda x: x.split('-')[0])

# 清理人数
df['人数'] = df['人数'].apply(lambda x: x.replace('人以上', ''))
df['人数'] = df['人数'].apply(lambda x: int(x.split('-')[0]))


# 清理注册资金
def cal(x):
    if '美元' in x:
        return float(x.split('万')[0]) * 7
    else:
        return float(x.split('万')[0])


df['注册资金'].fillna('0万元人民币', inplace=True)
df['注册资金'] = df['注册资金'].apply(lambda x: cal(x))

# # 清理成立时间
# df['成立时间'].fillna('0000-10-10', inplace=True)
# df['成立时间'] = df['成立时间'].apply(lambda x: int(x.split('-')[0]))

# df.to_excel(or_path('tttt'))
# exit()

import matplotlib.pyplot as plt
import matplotlib as mpl

# 用来正常显示中文标签
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
mpl.rcParams['axes.unicode_minus'] = False

# ----------查看互联网注册资金分布-----------------
df2 = df[df['成立时间'].notnull()]

s1 = df2.groupby('公司').size()
s2 = df2.groupby('公司')['注册资金'].mean()
s3 = df2.groupby('公司')['成立时间'].min()

df_dev = pd.DataFrame([s1, s2, s3]).T

# 数据清洗
df_dev['成立时间'] = df_dev['成立时间'].apply(lambda x: pd.to_datetime(x))
df_dev['注册资金'] = df_dev['注册资金'].apply(lambda x: float(x))
df_dev['Unnamed 0'] = df_dev['Unnamed 0'].apply(lambda x: int(x))

df_dev.reset_index(inplace=True)
df_dev.set_index('成立时间', inplace=True)

# 画图
df_dev[['注册资金']].plot()
plt.show()
print(df_dev.sort_values('注册资金',ascending=0).head())


# -------------------分布柱形图--------------------------------
df3 = df[df['薪水'] >= 8]
# print(df3.describe())
print(df3.head())

fig, axes = plt.subplots(5, 1, figsize=(18, 18))

area = df3.groupby('地区').size()
area.plot(kind='bar', color='k', grid=True, alpha=0.5, ax=axes[0])

exp = df3.groupby('经验要求').size()
exp.plot(kind='bar', color='b', grid=True, alpha=0.5, ax=axes[1])

edu = df3.groupby('学历要求').size()
edu.plot(kind='bar', color='y', grid=True, alpha=0.5, ax=axes[2])

ind = df3.groupby('行业').size()
ind.plot(kind='bar', color='g', grid=True, alpha=0.5, ax=axes[3])

inv = df3.groupby('融资').size()
inv.plot(kind='bar', color='c', grid=True, alpha=0.5, ax=axes[4])

plt.show()


import seaborn as sns

# -----------------不同行业下的融资情况-------------------

df4 = df[df['薪水'] >= 8]
inv2 = pd.DataFrame(df4.groupby(['行业', '融资']).size())
inv2.reset_index(inplace=True)
inv2 = pd.pivot_table(inv2, index='行业', columns='融资', values=0)
inv2.sort_index(inplace=True)

sns.heatmap(inv2)
plt.show()

print(inv2)
