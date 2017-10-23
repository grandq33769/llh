"""
To import birth data
"""

import re
import numpy as np
import pandas as pd
from llh.Python.data import BASE_PATH

PATH = BASE_PATH + '/Birth_Rate.csv'
COUNTY_ENG = {'花蓮': 'Hualien', '澎湖': 'Penghu', '彰化': 'Changhua',
              '臺東': 'Taitung', '宜蘭': 'Yilan', '嘉義': 'Chiayi',
              '金門': 'Kinmen', '雲林': 'Yunlin', '高雄': 'Kaohsiung',
              '屏東': 'Pingtung', '臺南': 'Tainan', '新竹': 'Hsinchu',
              '苗栗': 'Miaoli', '臺中': 'Taichung', '連江': 'Lienchiang',
              '南投': 'Nantou', '臺北': 'Taipei', '新北': 'New Taipei',
              '桃園': 'Taoyuan', '基隆': 'Keelung'}


def chin2eng():
    '''
    Give a dictionary with chinese taiwan county key and english name value
    Return: dict{Chinese:Eng}
    '''
    return COUNTY_ENG


def eng2chin():
    '''
    Give a dictionary with english taiwan county key and chinese name value
    Return: dict{Eng:Chinese}
    '''
    rdict = dict()
    for key, value in COUNTY_ENG.items():
        rdict.update({value: key})
    return rdict


def open_birth_rate():
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
    pattern = '.*[縣|市][^\(]'
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
        index = COUNTY_ENG[loc[-4:-2]]
        if loc[-2:-1] == '市':
            index += ' City'
        else:
            index += ' County'
        value = realframe.loc[18, loc].strip()[:-3].replace(',', '')
        rdict.update({index: int(value)})

    return rdict


if __name__ == '__main__':
    print(eng2chin())
