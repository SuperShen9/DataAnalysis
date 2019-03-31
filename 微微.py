# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
from build.Func import or_path
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

df = pd.read_excel(or_path('data'))

df.replace('阴性(-)', '', inplace=True)
df.replace(np.NaN, '', inplace=True)

result = pd.DataFrame()
for x in range(df.shape[0]):
    list1 = []
    for y in df.columns[1:]:

        if df.loc[x, y] != '':
            list1.append(y[:5].strip() + '+')
    if len(list1) == 0:
        result.loc[x, '结果'] = np.NaN
    else:
        result.loc[x, '结果'] = ", ".join(list1)

result.fillna('阴性', inplace=True)
print(result.groupby('结果').size())

result.to_excel(or_path('ttt'))



