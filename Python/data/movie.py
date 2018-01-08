'''
To import movie data as python data structure from .csv
Date : 2017/12/31
'''
import os
import sys
import ast
import re
import numpy as np
import pandas as pd

BASE_PATH = '/Users/lhleung/Documents/Data/the-movies-dataset'
CSV = ['credits', 'keywords', 'links', 'movies_metadata', 'ratings']
PATH = {}

for csv in CSV:
	name = '.'.join([csv, 'csv'])
	path = '/'.join([BASE_PATH, name])
	PATH.update({csv: path})
	if not os.path.isfile(path):
		raise IOError(name + 'is not exist !!')

def read(attr):
	'''
	Args:
		attr(string): Attribute name of .csv file
	Returns:
		dfm(pd.Dataframe): Pandas dataframe of that csv
							and finish filling na value
	'''
	path = PATH[attr]
	print(path)
	dfm = pd.read_csv(path, header=0)
	process_na(dfm)

	return dfm


def process_na(dataframe):
	'''
	Args:
		dataframe(pd.DataFrame): Dataframe needed to process null value
	'''
	for attr in dataframe.columns:
		# print(attr,dfm[attr].dtype)
		if dataframe[attr].dtype != np.object:
			dataframe[attr].fillna(0, inplace=True)
		else:
			dataframe[attr].fillna('None', inplace=True)
			dataframe[attr] = dataframe[attr].str.replace('\[\]', 'None')

def open_credits():
	'''
    Input credits datas
    Returns:
		dfm(pd.Dataframe): Processed dataframe of credits
		Finish dtype converting, set_index, dropping tuple and columns
    '''

	dfm = read('credits')
	dfm.set_index('id', inplace=True)

	condition = (dfm.crew == 'None') & (dfm.cast == 'None')
	dfm.drop(dfm[condition].index, inplace=True)

	return dfm

def convert_attr(dataframe, index, attr, dict_attr):
	if isinstance(dataframe[attr].loc[index], list):
		contents = [t[dict_attr] for t in dataframe[attr].loc[index]]

	elif isinstance(dataframe[attr].loc[index], dict):
		contents = dataframe[attr].loc[index][dict_attr]

	set_attr(dataframe, index, attr, ','.join(contents))

def set_attr(dataframe, index, attr, value):
	dataframe.at[index, attr] = value
	
def open_movies_metadata():
	'''
    Input movies_metadata datas
    Returns:
		dfm(pd.Dataframe): Processed dataframe of movies_metadata
		Finish dtype converting, set_index, dropping tuple and columns
    '''
	dfm = read('movies_metadata')
	# print(dfm.isnull().values.any())

	print('Dtype converting ... ')
	cattr = ['budget', 'id', 'popularity', 'vote_count', 'runtime', 'revenue']
	dtype = ['int64', 'int64', 'float64', 'int64', 'int64', 'int64']	
	
	for a,t in zip(cattr,dtype):
		try:
			dfm[a] = dfm[a].str.replace(r'[\D]+', '0')
		except AttributeError:
			pass
		dfm[a] = dfm[a].astype(t)

	dfm['popularity'].fillna(0, inplace=True)
	# print(dfm['budget'].dtype)

	dfm.drop_duplicates(subset='id', inplace=True)
	dfm.set_index('id', inplace=True)
	'''
	Drop Conditions
	1. budget < 1000 (NO)
	2. revenue < 1000 (NO)
	3. status == None
	4. movie.id in credit.id (Do on outside)
	'''
	conditions = [dfm.status == 'None']
	for con in conditions:
		dfm.drop(dfm[con].index, inplace=True)

	# Convert attribute
	cattr = ['belongs_to_collection', 'spoken_languages', 'genres', 'production_companies', 
			 'production_countries']
	dattr = ['name', 'iso_639_1', 'name', 'name', 'name']

	for attr, dattr in zip(cattr, dattr):
		print('Convert Attribute ... \'{}\' from \'{}\''.format(attr, dattr))
		dfm[attr] = dfm[attr].apply(ast.literal_eval)
		convert = lambda x: convert_attr(dfm, x, attr, dattr)
		dfm[dfm[attr].notnull()].index.map(convert)

	print('Dropping Attributes ...')
	# Drop Column
	dcols = [
					'belongs_to_collection', 'homepage', 'imdb_id', 'overview', 'poster_path',
					'status', 'tagline', 'video'
	]
	dfm.drop(dcols, axis=1, inplace=True)
	print(dfm)
	print(dfm.dtypes)
	return dfm


if __name__ == '__main__':
	datas = open_movies_metadata()
	#datas.to_csv(BASE_PATH+'/movies_metadata_2.csv')
