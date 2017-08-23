"""
To import birth data
"""

import os
import re
import numpy as np
import pandas as pd

BASE_URL = os.path.dirname(__file__)
print(BASE_URL)
PATH = BASE_URL + '/Birth_Rate.csv'


def open():
    '''
    Input & Modify data
    '''
    dataframe = pd.read_csv(PATH, header=1)
    dataframe = dataframe.rename(columns={'Unnamed: 0': '年份'})
    dataframe = dataframe.loc[:, '年份':'總生育率 / 連江縣 ']

    '''Print Column'''
    # print(dataframe.loc[18])
    '''取代'''
    # print(dataframe.replace('-', '0'))
    '''全數字 indexing'''
    # print(dataframe.iloc[18][3])
    '''將所有空值轉換'''
    to_replace = dataframe.iloc[18][3]
    dataframe = dataframe.replace(to_replace, np.nan)
    ''' 存在的顯示 '''
    # dataframe2 = dataframe[dataframe.isin([to_replace])]
    ''' 檢查 Match Pattern '''
    pattern = '.*縣[^\(]'
    # print(re.match(pattern, '台南縣'))
    alist = [a for a in dataframe.columns[:2]] + \
        [a for a in dataframe.columns if re.match(pattern, a)]
    realframe = dataframe[alist]
    for att in realframe.columns[2:]:
        nlist = pd.isnull(realframe[att])
        if any(nlist):
            # print('Null: ', att)
            pattern = '.*' + att[-4:-2] + '市[^(]'
            clist = [
                loc for loc in dataframe.columns if re.match(pattern, loc)]
            # print('Next: ', clist)
            for index in [i for i, x in enumerate(nlist) if x]:
                realframe.loc[index, att] = dataframe.loc[index, clist[0]]

    rdict = dict()
    for loc in realframe.columns[2:]:
        index = loc[-4:-1]
        value = realframe.loc[18, loc].strip()[:-3].replace(',', '')
        rdict.update({index: int(value)})

    return rdict


if __name__ == '__main__':
    open()
