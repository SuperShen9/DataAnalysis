# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
from build.Func import or_path
import warnings

from efficient_apriori import apriori

warnings.filterwarnings('ignore')

# 设置数据集

data = [['香蕉', '尿布', '啤酒'],['尿布', '啤酒', '鸡蛋'],['菊花', '尿布']]

# 挖掘频繁项集和频繁规则

itemsets, rules = apriori(data, min_support=0.5, min_confidence=1)
print('\n')
print(itemsets)
print(rules)

exit()

#
# # # 官网案例
# transactions = [['eggs', 'bacon', 'soup'],
#                 ['eggs', 'bacon', 'apple'],
#                 ['soup', 'bacon', 'banana']]
#
# # print(type(transactions))
# # exit()
# itemsets, rules = apriori(transactions, min_support=0.5, min_confidence=1)
# print(itemsets)
# print(rules)
# exit()

df = pd.read_excel(or_path('\wx\张艺谋合作影视明星 - 副本'))

df['name2'] = df['name'].apply(lambda x: x.split(' / ')[1:])

data = df['name2'].tolist()
# print(type(data))
# print(data)
# exit()

itemsets, rules = apriori(data, min_support=0.5, min_confidence=1)
print(itemsets)
print(rules)
