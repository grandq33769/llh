"""To import birth data"""

import os
import re
import numpy as np
import pandas as pd

BASE_URL = os.path.dirname(__file__)
print(BASE_URL)
PATH = BASE_URL + '/Birth_Rate.csv'

df = pd.read_csv(PATH, header=1)
df = df.rename(columns={'Unnamed: 0': '年份'})
df = df.loc[:, '年份':'總生育率 / 連江縣 ']

'''Print Column'''
# print(df.loc[18])
'''取代'''
# print(df.replace('-', '0'))
'''全數字 indexing'''
# print(df.iloc[18][3])
'''將所有空值轉換'''
to_replace = df.iloc[18][3]
df = df.replace(to_replace, np.nan)
''' 存在的顯示 '''
# df2 = df[df.isin([to_replace])]
''' 用regex移除欄位 '''
pattern = '.a'
print(re.match(pattern, 'aa'))
# alist = [a for a in df.columns if re.match(pattern, a)]
# print(alist)
# df = df[alist]

# print(df)
