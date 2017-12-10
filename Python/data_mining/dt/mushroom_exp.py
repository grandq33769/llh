'''
Decision tree experiment(Data minig project 2) using mushroom dataset
Date: 2017/12/1
'''
'''
Golden Rules:
1. Warts or scales on the cap.(cap-surface:fibrous&scaly)
2. A parasol or umbrella shaped cap.(cap-shaped:convex)
3. The presence of a bulbous cup or sac around the base.(stalk-root:bulbous&cup)
4. A white spore print.(spore-print-color:white)
5. The presence of a ring around the stem.(ring-number:one&two)
6. Gills that are thin and white.(gill-size:narrow;gill-color:white)
'''
'''
Data Attribute:
['class' 'cap-shape' 'cap-surface' 'cap-color' 'bruises' 'odor'
 'gill-attachment' 'gill-spacing' 'gill-size' 'gill-color' 'stalk-shape'
 'stalk-root' 'stalk-surface-above-ring' 'stalk-surface-below-ring'
 'stalk-color-above-ring' 'stalk-color-below-ring' 'veil-type' 'veil-color'
 'ring-number' 'ring-type' 'spore-print-color' 'population' 'habitat']
'''
import sys
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_score, recall_score, f1_score
import graphviz
import numpy as np

PATH = '~/Documents/Data/mushrooms.csv'
CON_DICT = {
				'cap-surface': ['f', 'y'],
				'cap-shape': ['x'],
				'stalk-root': ['b', 'u'],
				'spore-print-color': ['w'],
				'ring-number': ['o', 'r'],
				'gill-size': ['n'],
				'gill-color': ['w']
}


def open_mushroom(prop):
	'''
    Args:
            prop(float): Training data proportion in range (0,1]
            num_a(int): Number of attributes used to return
    Returns:
            tr_x(Dataframe): Training input data dictionery
            tr_y(list): Training target output
            te_x(Dataframe): Testing input data dictionery
            te_y(list): Testing target output
    '''
	mdf = pd.read_csv(PATH, header=0)
	train_index = int(len(mdf.index) * prop) - 1
	# print(mdf.columns.values)

	train = mdf.iloc[:train_index]
	tr_x = train.iloc[:, 1:]
	tr_y = train['class'].values.tolist()

	test = mdf.iloc[train_index + 1:]
	te_x = test.iloc[:, 1:]
	te_y = test['class'].tolist()

	return tr_x, tr_y, te_x, te_y


def golden_classify(mushroom):
	'''
    Args:
            mushroom(Dataframe): A mushroom tuple
    Returns:
            type(char): e for edible, p for poisonious
    '''
	for k, v in CON_DICT.items():
		for ans in v:
			try:
				if mushroom[k] == ans:
					return 'p'
			except:
				continue

	return 'e'


def vectorize(inputs, target):
	'''
	Args:
			inputs(pandas.Dataframe): Mushroom input data
			target(list): Target output class
	Returns:
			vect(DictVectorizer): DictVectorizer fit by feature 
			le(LabelEncoder): LabelEncoder fit by target class
	'''
	#Input Vectorization
	x_dict = inputs.T.to_dict().values()
	vect = DictVectorizer()
	x = vect.fit_transform(x_dict)
	print('\nNumber of attribute:' + str(len(vect.get_feature_names())))

	#Label Encode
	le = LabelEncoder()
	y = le.fit_transform(target)
	print('Lenght of data:' + str(len(y)))
	print('Target Domain:' + str(le.classes_))

	return vect, le


def show(name, clf, fn, cn):
	'''
	Args:
			clf(sklearn.tree.DecisionTreeClassifier):
				Decision Tree Classifier
			fn(list): Features names
			cn(list): Classes names
	Output:
			graph(graphviz.Source): Result of graph represent the graph
	'''
	dot_data = tree.export_graphviz(
					clf,
					out_file=None,
					feature_names=fn,
					class_names=cn,
					filled=True,
					rounded=True,
					special_characters=True)
	graph = graphviz.Source(dot_data)
	graph.render(name)


def evaluate(true, test):
	'''
	Args:
			true(list): True labels
			test(list): Test labels predicted by classifier
	Output:
			precision(float): Macro precision score(TP/TP+FP)
			recall(float): Macro recall score(TP/TP+FN)
			f1_score(float): Macro F1 score
			(2*((precision*recall)/(precision+recall))
	'''
	precision = precision_score(true, test, average='macro')
	recall = recall_score(true, test, average='macro')
	f1s = f1_score(true, test, average='macro')
	print('Precision: ', precision)
	print('Recall: ', recall)
	print('Macro F1 Score: ', f1s)

	return precision, recall, f1s


def run_exp(tr_x, tr_y, te_x, te_y):
	'''
	Args:
		tr_x(DataFrame): Trainig input dataframe
		tr_y(list): Training target data
		te_x(DataFrame): Testing input dataframe
		te_y(list): Testing target data
	'''
	#Testing golden_rule
	g_result = list()
	for _, tup in te_x.iterrows():
		y = golden_classify(tup)
		g_result.append(y)

	#Pre-process
	dv, le = vectorize(tr_x, tr_y)
	str_num = str(len(tr_x.columns.values))
	str_size = str(len(tr_x))
	tr_x = dv.transform(tr_x.T.to_dict().values())
	tr_y = le.transform(tr_y)
	te_x = dv.transform(te_x.T.to_dict().values())

	#Build decision tree
	dt = tree.DecisionTreeClassifier()
	dt = dt.fit(tr_x, tr_y)
	filename = 'Decision Tree_' + str_num + '-' + str_size
	show(filename, dt, dv.get_feature_names(), le.classes_)

	#Testing decision tree
	dt_result = dt.predict(te_x)
	dt_result_labels = le.inverse_transform(dt_result)

	#Build random forest
	rf = RandomForestClassifier()
	rf = dt.fit(tr_x, tr_y)
	filename = 'Random Forest_' + str_num + '-' + str_size
	show(filename, rf, dv.get_feature_names(), le.classes_)

	#Testing random forest
	rf_result = rf.predict(te_x)
	rf_result_labels = le.inverse_transform(rf_result)

	#Evaluation
	print('\n Golden Classifier Result-' + str_num + '-' + str_size)
	evaluate(te_y, g_result)
	print('\n Decision Tree Result-' + str_num + '-' + str_size)
	evaluate(te_y, dt_result_labels)
	print('\n Random Forest Result-' + str_num + '-' + str_size)
	evaluate(te_y, rf_result_labels)


if __name__ == '__main__':
	#Drop attribute experiment
	TR_X, TR_Y, TE_X, TE_Y = open_mushroom(0.7)
	attr = TR_X.columns.values
	filter_tr_x = TR_X
	filter_te_x = TE_X

	for attr in CON_DICT:
		#Drop 1 attribute each time
		filter_tr_x = filter_tr_x.drop([attr], axis=1)
		filter_te_x = filter_te_x.drop([attr], axis=1)

		run_exp(filter_tr_x, TR_Y, filter_te_x, TE_Y)

	#Data size experiment
	for size in np.linspace(0.7, 0.1, 7):
		TR_X, TR_Y, TE_X, TE_Y = open_mushroom(size)
		run_exp(TR_X, TR_Y, TE_X, TE_Y)
