'''
Decision tree experiment(Data minig project 2) using mushroom dataset
Date: 2017/12/1
'''
import pandas as pd

PATH = '~/Documents/Data/mushrooms.csv'

def open_mushroom(prop, num_a=0):
	'''
	Args:
		prop(float): Training data proportion in range (0,1]
		num_a(int): Number of attributes used to return
	Returns:
		train(list): Training data list
		test(list): Testing data list
	'''
	mdf = pd.read_csv(PATH, header=0)
	train_index = int(len(mdf.index)*prop) - 1

	train = mdf.iloc[:train_index].values.tolist()
	test = mdf.iloc[train_index+1:].values.tolist()

	return train, test

if __name__ == '__main__':
	x, y = open_mushroom(0.7)
	print(x)
	print(y)
