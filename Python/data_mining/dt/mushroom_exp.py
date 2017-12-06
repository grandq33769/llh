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
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
import graphviz

PATH = '~/Documents/Data/mushrooms.csv'


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
	if mushroom['cap-surface'] == 'f' or mushroom['cap-surface'] == 'y':
		return 'p: Rule 1'
	elif mushroom['cap-shape'] == 'x':
		return 'p: Rule 2'
	elif mushroom['stalk-root'] == 'b' or mushroom['stalk-root'] == 'u':
		return 'p: Rule 3'
	elif mushroom['spore-print-color'] == 'w':
		return 'p: Rule 4'
	elif mushroom['ring-number'] == 'o' or mushroom['ring-number'] == 't':
		return 'p: Rule 5'
	elif mmushroom['gill-size'] == 'n' or ushroom['gill-color'] == 'w':
		return 'p: Rule 6'
	else:
		return 'e'


def train(inputs, target):
	'''
	Args:
			inputs(pandas.Dataframe): Mushroom input data
			target(list): Target output class
	Returns:
			tree(sklearn.tree.DecisionTreeClassifier()): 
				Decision tree trained by arguments
			fn(list): Features names
			cn(list): Classes names
	'''
	#Input Vectorization
	x_dict = inputs.T.to_dict().values()
	vect = DictVectorizer()
	x = vect.fit_transform(x_dict)
	fn = vect.get_feature_names()
	print('Number of attribute:' + str(len(fn)))

	#Label Encode
	le = LabelEncoder()
	y = le.fit_transform(target)
	print('Lenght of data:' + str(len(y)))
	print('Target Domain:' + str(le.classes_))

	#Build model
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(x, y)

	return clf, fn, le.classes_


def show(clf, fn, cn):
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
	graph.render('mushroom')


if __name__ == '__main__':
	TR_X, TR_Y, TE_X, TE_Y = open_mushroom(0.7)

	#golden_rule
	'''
	g_result = list()
	for inx, tup in TR_X.iterrows():
		y = golden_classify(tup)
		g_result.append(y)
	'''

	#Build Decision Tree
	dt, fn, cn = train(TR_X, TR_Y)
	show(dt, fn, cn)
