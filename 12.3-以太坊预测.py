# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']

import warnings

warnings.filterwarnings('ignore')

# 重新读取数据
df = pd.read_hdf('E:\BaiduYunDownload\weixin\ARMA_ETH\ETH_USDT_day.h5')

# 查看数据
print(df.info())

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

# 打印结果
print(result, '\n')

aic_min = result.index.min()
opt_para = result.loc[aic_min, 0]

print('最小AIC: ', aic_min)
print('最优参数: ', opt_para)

# 提取前75%数据
n = int(df.shape[0] * 0.75)
df1 = df.head(n)['close']

# 数据拟合
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
