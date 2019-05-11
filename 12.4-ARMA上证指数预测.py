# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']

import warnings

warnings.filterwarnings('ignore')

# 重新读取数据
df = pd.read_csv('E:\BaiduYunDownload\weixin\ARMA_SZ\szzs.csv')

# 查看数据
print(df.head())
print('-' * 50)
print(df.info())
print('-' * 50)

# 转化时间类型
df['Timestamp'] = df['Timestamp'].apply(lambda x: pd.to_datetime(x))

# 截取时间点
df = df[df['Timestamp']< pd.to_datetime('2014-01-01')]

# 设置索引
df.set_index('Timestamp',inplace=True)

# 时间周期转换
df = df.resample('M').mean()

# df = df.resample('Q-DEC').mean()

# plt.plot(df)
# plt.show()
# exit()


from itertools import product

# 设置参数范围
ps = range(0, 2)
qs = range(0, 2)
parameters = product(ps, qs)
parameters_list = list(parameters)

print(parameters_list)
print('-' * 50)

# 导入模块
from statsmodels.tsa.arima_model import ARMA

# 筛选最优参数
result = []
for param in parameters_list:
    try:
        model = ARMA(df.Price, order=(param[0], param[1])).fit()
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
n = int(df.shape[0] * 0.85)
df1 = df.head(n)['Price']

# 数据拟合
arma = ARMA(df1, order=opt_para).fit()

# 模型预测
predict_y = arma.predict(start=n, end=df.shape[0])

# 以太坊预测结果显示
plt.figure(figsize=(14, 7))
df['Price'].plot(label='实际金额')
predict_y.plot(color='r', ls='--', label='预测金额')
plt.legend()
plt.title('上证指数价格')
plt.xlabel('时间')
plt.ylabel('RMB')
plt.show()
