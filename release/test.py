# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

print(type(np.array(a)))
print(np.array(a))
print('-' * 50)
print(type(np.mat(a)))
print(np.mat(a))
