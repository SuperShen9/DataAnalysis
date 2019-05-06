# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
from build.Func import or_path, hash_data

df = pd.read_excel(or_path('HPV07原始数据'))


def biao1(df):
    df['结果2'] = df['结果'].apply(lambda x: x.split(','))

    list1 = []
    for x in range(df.shape[0]):
        if df.loc[x, '结果'] != '阴性':
            list1 = list1 + df.loc[x, '结果2']

    s1 = pd.DataFrame(list1)
    s1.replace(' ', inplace=True)

    s1 = pd.DataFrame(s1.groupby(0).size())
    s1.columns = ['阳性例数']
    s1.reset_index(inplace=True)

    s1.columns = ['HPV类型', '阳性例数']

    s1['构成比'] = round(s1['阳性例数'] / s1['阳性例数'].sum() * 100, 2)
    s1['阳性率'] = round(s1['阳性例数'] / df.shape[0] * 100, 2)

    df2 = pd.read_excel(or_path('MAP'))

    df = pd.merge(s1, df2, on='HPV类型', how='left')

    df['类型'] = df['类型'].fillna('高危型')

    df.to_excel(or_path('HPV各型的阳性例数'))


def biao2():
    def age(x):
        if x <= 10:
            return '0-10'
        elif x <= 30:
            return '10-30'
        elif x <= 50:
            return '30-50'
        elif x <= 70:
            return '50-70'
        elif x <= 90:
            return '70-90'


    df['年龄2'] = df['年龄'].apply(lambda x: age(x))


    s1 = pd.DataFrame(df.groupby('年龄2').size())
    s1.columns = ['个数']

    df2 = df[(df['TCT'] == 'L') | (df['TCT'] == 'H') | (df['TCT'] == 'A')]
    s1['TCT阳性'] = df2.groupby('年龄2').size()

    df3 = df[(df['HPV阳性'].notnull())]
    s1['HPV阳性'] = df3.groupby('年龄2').size()

    df4 = df[(df['感染层'] == '单一感染')]
    s1['单一感染'] = df4.groupby('年龄2').size()

    df5 = df[(df['感染层'] == '多重感染')]
    s1['多重感染'] = df5.groupby('年龄2').size()

    s1.fillna(0,inplace=True)

    s1.loc['汇总'] = s1.apply(lambda x: sum(x))


    def more(col):
        s1[col] = s1[col].apply(lambda x: str(int(x))) + '(' + (s1[col] / s1['个数']).apply(
            lambda x: str('%.2f%%' % (x * 100))) + ')'


    more('TCT阳性')
    more('HPV阳性')
    more('单一感染')
    more('多重感染')

    s1['个数'] = s1['个数'].apply(lambda x: str(int(x))) + '(' + (s1['个数'] / 714).apply(
            lambda x: str('%.2f%%' % (x * 100))) + ')'

    s1.reset_index(inplace=True)
    s1.rename(columns={'年龄2':'年龄(岁)'},inplace=True)

    s1.to_excel(or_path('各个年龄阶段的总数以及总计'),index=False)
    print(s1)

biao2()
exit()


df3 = df[(df['HPV阳性'].notnull())]

df3=pd.DataFrame(df3.groupby('TCT').size())
df3.columns=['Hpv阳性个数（＋阳性率）']

df4=pd.DataFrame(df.groupby(['感染层','TCT阳性']).size())
df4.columns=['TCT阳性个数（+阳性率）']

df3.to_excel(or_path('Hpv阳性个数（＋阳性率）'))
df4.to_excel(or_path('TCT阳性个数（+阳性率）'))

print(df4)