import pandas as pd
import json
import time
from itertools import product
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--source', dest='source')

args = parser.parse_args()

FILE = args.source
COLUMN_NEED = ['area','cunli','Ym','gen']
# YEAR = [10501, 10502]
SUFFIX_NAME = '_village.json'

def read(path):
    # Read energy data by using pandas
    '''
    Input: .csv path
    Output: pandas.Dataframe
    '''
    return pd.read_csv(path)

def purn(df):
    # Purning out all unused column
    '''
    Input: pandas.Dataframe
    Output: pandas.Dataframe
    '''
    return_df = pd.DataFrame()
    for attr in COLUMN_NEED:
        return_df = pd.concat([return_df, df[attr]], axis=1)
    return return_df

def replace(df, attr, old, new):
    # Replace a target value to a new value in specific attribute column
    '''
    Input:
        df: pandas.Dataframe
        attr: Attribute name for column
        old: to replace value
        new: replaced value
    Output: pandas.Dataframe
    '''
    df[attr] = df[attr].apply(lambda x: x.replace(old, new))
    return df


def combine(df, attrs, new_name):
    # Combine the column in attrs list
    '''
    Input: 
        df: pandas.Dataframe
        attrs: Attribute name needed to combine
        new_name: New column name
    Output:
        df: Combined attribute dataframe
    '''
    df[new_name] = df[attrs].apply(lambda x: ''.join(x), axis=1)
    df = df.drop(columns = attrs)
    return df

def seperate(df, attr):
    # Seperate dataframe into serval dataframe by input attribute
    '''
    Input: pandas.DataFrame
    Output: Lists of pandas.DataFrame
    '''
    attr_set = set(df[attr].tolist())
    return {a:df.loc[df[attr] == a] for a in attr_set}

def convert_dict(df, attrs, key):
    # Convert the dataframe to dictionary with corr. attr value by the same key
    '''
    Input: 
        df: pandas.DataFrame
        attrs: Attribute name list to include in dict
        key: Key attribute name to clustering
    Output:
        return_dict: {key: sum_value}
    '''    
    keys = list(set(df[key].tolist()))
    return_dict = {k:{} for k in keys} 
    for k,a in product(keys, attrs):
        values = _sum(df, key, k, a)
        return_dict[k].update({a:values})
    return return_dict

def _sum(df, key, k, attr):
    # Sum up attr by specific k value in key attribute
    same = df.loc[df[key] == k]
    return sum(same[attr])

if __name__ == '__main__': 

    data = read(FILE)
    # print(data)
    # print(set(data['area'].tolist()))
    # print(set(data.loc[data['area'] == '學甲區']['cunli'].tolist()))
    data = purn(data)
    # print(type(data['area']))
    data = replace(data, 'cunli', '村', '里')
    data = replace(data, 'cunli', '■', '部')
    data = replace(data, 'cunli', '部榔', '糠榔')
    data = combine(data, ['area', 'cunli'], 'village')
    # print(data.loc[data['village'] == '東山區南勢里'])
    # print(data.loc[data['Ym'] == 10501])
    # data_dict = seperate(data, 'Ym')
    # print(data)
    # for yr in YEAR:
    result = convert_dict(data, ['gen'], 'village')
    for village,gen in sorted(result.items(), key=lambda kv: -kv[1]['gen']):
        print(village,gen)

    result.update({"updateAt":time.strftime("%Y/%m/%d", time.localtime())})
    name = ''.join(c for c in FILE if c.isdigit())
    if '上' in FILE:
        name += 'up'
    elif '下' in FILE:
        name += 'down'
    with open(name+SUFFIX_NAME, 'w', encoding='unicode-escape') as wf:
        json.dump(result, wf, ensure_ascii=False)
    with open(name+'村名.txt', 'w') as wf:
        wf.writelines('\n'.join(result.keys()))
