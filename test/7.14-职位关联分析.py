# -*- coding: utf-8 -*-
# author：Super
from efficient_apriori import apriori
import pandas as pd
import matplotlib.pyplot as plt
from build.Func import or_path

# 读取数据
df = pd.read_excel(or_path('聚类结果'))

df.reset_index(inplace=True)

# print(df.head())
# exit()

df1 = pd.DataFrame(df.groupby('K-Means聚类').apply(lambda x: list(x['index'])))
df2 = pd.DataFrame(df.groupby('EM聚类').apply(lambda x: list(x['index'])))

df = df1.append(df2, ignore_index=True)

# print(df)
# exit()

from efficient_apriori import apriori

df = df[0].tolist()


for i in df:
    print(type(i))
    print(i)

exit()




itemsets, rules = apriori(df, min_support=0.5, min_confidence=1)

print(itemsets)
print(rules)

exit()

print(df)
