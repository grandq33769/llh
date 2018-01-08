from collections import namedtuple
from itertools import tee
import numpy as np
import pandas as pd
from orangecontrib.associate.fpgrowth import * 

BOUNDARY = namedtuple('Boundary', ['max', 'min'])
LEVELS = list(range(1,16))

FILE_PATH = ('movies_metadata_2.csv')

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
	print('{} max:{} min:{}'.format(values.name, bound.max, bound.min))
	intervals = list(np.linspace(bound.min, bound.max, len(LEVELS) + 1))
	print('Intervals:',intervals)
	return values.transform(lambda x: (x - bound.min) / (bound.max - bound.min))


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
	transformed = inputs.transform(lambda x, i=intervals: _project(x, intervals))
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

def _split(value):
	'''
	Args:
		value(string): contents to be splited ','
	Returns:
		(list): Return list contain splited attributes value 		
	'''
	split = value.split(':')
	header = split[0]	
	contents = split[1].split(',')
	return  [':'.join([header,c]) for c in contents]

def split(dataframe):
	'''
	Args:
		dataframe(pd.DataFrame): Dataframe that needed to split column
	Returns:
		r_list(list): Returned list containing splited tuple
	'''
	r_list = []
	for t in dataframe.values:
		t_list = []
		for v in t:
			t_list.extend(_split(v))
		r_list.append(tuple(t_list))

	return r_list

def preprocess(projection=True, attr_n=True):
	'''
	Preprocessing of movies_metadata
	1. Change all numerical to categorical
	2. Append attribute name to each value
	3. Change each tuple to transaction
	'''
	dfm = pd.read_csv(FILE_PATH)
	# dfm.drop(['title', 'original_title'], axis=1, inplace=True)
	dfm.set_index('id', inplace=True)
	
	min_v = min(dfm['release_date'])
	dfm['release_date'] = dfm['release_date'].replace('None', str(min_v))
	dfm['release_date'] = dfm['release_date'].transform(lambda x: x[:4])
	dfm['release_date'] = dfm['release_date'].astype('int64')

	dfm[dfm.release_date > 2017].to_csv('exception.csv')
	for attr in dfm.columns:
		if dfm[attr].dtype == np.int64 or dfm[attr].dtype == np.float64:
			dfm[attr] = rescale(dfm[attr])
			if projection:
				dfm[attr] = project(dfm[attr], LEVELS)
		if attr_n:
			dfm[attr] = dfm[attr].transform(lambda x, a=attr: a + ':' + str(x))

	return split(dfm)

if __name__ == '__main__':
	clean = preprocess()
	itemsets = dict(frequent_itemsets(clean, 0.05))
	# print(itemsets)
	rules = list(association_rules(itemsets, 0.9))
	'''
	for rule in rules:
		print(rule)
	'''	
