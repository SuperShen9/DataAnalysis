# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
from build.Func import or_path

import warnings

warnings.filterwarnings('ignore')

##csv转化为h5
# df = pd.read_csv('E:\BaiduYunDownload\weixin\ARMA_ETH\ETH_USDT.csv')
# df.to_hdf('E:\BaiduYunDownload\weixin\ARMA_ETH\ETH_USDT.h5',key='data')

##读取h5文件
# df = pd.read_hdf('E:\BaiduYunDownload\weixin\ARMA_ETH\ETH_USDT.h5')

## 查看数据
# print(df.info())

# # 转换时间格式
# df['date'] = df['date'].apply(lambda x: pd.to_datetime(x))
#
# # 设置为索引
# df.set_index('date', inplace=True)
#
# # 按天统计数据
# df_day = df.resample('D').mean()
#
# # 导出数据
# df_day.to_hdf('E:\BaiduYunDownload\weixin\ARMA_ETH\ETH_USDT_day.h5',key='data')

# # 走势图
# plt.plot(df_day['close'])
#
# plt.show()

# 重新读取数据
df = pd.read_hdf('E:\BaiduYunDownload\weixin\ARMA_ETH\ETH_USDT_day.h5')

# 按周统计数据
df = df.resample('M').mean()

# # 走势图
# plt.plot(df_w['close'])
#
# plt.show()

from itertools import product

# 设置参数范围
ps = range(0, 3)
qs = range(0, 3)
parameters = product(ps, qs)
parameters_list = list(parameters)

print(parameters_list)

# 导入模块
from statsmodels.tsa.arima_model import ARMA

# 筛选最优参数
result = []
for param in parameters_list:
    try:
        model = ARMA(df.close, order=(param[0], param[1])).fit()
    except ValueError:
        print('参数错误:', param)
        continue

    aic = model.aic
    result.append([param, aic])

# 用df形式输出
result = pd.DataFrame(result)
result.set_index(1, inplace=True)

print(result, '\n')

aic_min = result.index.min()
opt_para = result.loc[aic_min, 0]

print('最小AIC: ', aic_min)
print('最优参数: ', opt_para)

# 提取前75%数据
n = int(df.shape[0] * 0.75)
df1 = df.head(n)['close']

arma = ARMA(df1, order=opt_para).fit()

# 模型预测
predict_y = arma.predict(start=n, end=df.shape[0])


# 以太坊预测结果显示
plt.figure(figsize=(14, 7))
df['close'].plot(label='实际金额')
predict_y.plot(color='r', ls='--', label='预测金额')
plt.legend()
plt.title('以太坊金额')
plt.xlabel('时间')
plt.ylabel('美金')
plt.show()
