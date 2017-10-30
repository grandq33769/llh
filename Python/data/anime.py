'''
To import anime data as python data structure from .csv
Date : 2017/10/23
'''
from collections import namedtuple
from itertools import tee
import logging as log
import numpy as np
import pandas as pd
from llh.Python.data import BASE_PATH

DATA_PATH = BASE_PATH + '/Anime/anime.csv'
BOUNDARY = namedtuple('Boundary', ['max', 'min'])
LEVELS = ['Low', 'Below Average', 'Average', 'Above Average', 'High']


def open_data(standardize, projection=True, attr_n=True):
    '''
    Input & Rescalling Anime data
    Place .csv path in __init__.py
    Args:
        standardize(func): Function to standardize the numeric
        projection(boolean): True for project to LEVELS string
        attr_n(boolean): True for adding attribute name in value
    Returns:
        rli(tuple): Return tuple include all transaction tuple
    '''
    dfm = pd.read_csv(DATA_PATH, header=0)
    dfm = dfm.loc[:, 'genre':'members']
    dfm = dfm.replace('Unknown', '1').fillna('0')

    for attr in dfm.loc[:, 'episodes':'members']:
        values = dfm[attr].transform(float)
        dfm[attr] = standardize(values)
        if projection:
            dfm[attr] = project(dfm[attr], LEVELS)
        if attr_n:
            dfm[attr] = dfm[attr].transform(lambda x, a=attr: a + ':' + str(x))

    rli = list()
    for _, tup in dfm.iterrows():
        tli = list()
        try:
            tli.extend(tup['genre'].split(', '))
        except AttributeError:
            tli.append('NaN')
        tli.extend(tup['type':'members'])
        rli.append(tuple(tli))
    log.info('Anime data open successful ... Data lenght: %d', len(rli))
    return tuple(rli)


def rescale(values):
    '''
    Rescaling the value between [0,1] depends on data max & min
    Args:
        values(DataFrame): Values of Data Frame to be rescale
    Returns:
        values(DataFrame): Transformed Data Frame by rescalling value
        (x - values.min / values.max - values.min)
    '''
    bound = BOUNDARY(max(values), min(values))
    return values.transform(
        lambda x: (x - bound.min) / (bound.max - bound.min))


def zscore(values):
    '''
    Args:
        values(DataFrame): Values to be rescale
    Returns:
        values(DataFrame): Transformed Data Frame by z-score value
        (x - values.mean/ values.std)
    '''
    mean = np.mean(values)
    std = np.std(values)
    return values.transform(lambda x: (x - mean) / std)


def project(inputs, targets):
    '''
    Args:
        inputs(Dataframe): pandas.Dataframe contain data to be projected
        targets(list): Target string to be output corresponding to its original value
    Returns:
        rdfm(Dataframe): pandas.Dataframe contain projected data
    '''
    bound = BOUNDARY(max(inputs), min(inputs))
    intervals = list(np.linspace(bound.min, bound.max, len(targets) + 1))
    transformed = inputs.transform(
        lambda x, i=intervals: _project(x, intervals))
    return transformed.transform(lambda x: targets[x])


def _project(value, intervals):
    '''
    Args:
        value(float): float value to be projected
        intervals(list): Intervals range from np.linspace depends on the LEVELS
    Retruns:
        index(int):  Index of intervals that the value belong to
    '''
    for small, large in pairwise(intervals):
        if small <= value <= large:
            return intervals.index(small)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    first, second = tee(iterable)
    next(second, None)
    return zip(first, second)


if __name__ == '__main__':
    open_data(zscore)
