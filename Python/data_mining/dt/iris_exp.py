'''
Script for building decision tree
Date: 2017/12/1
'''

from sklearn.datasets import load_iris

DATA = load_iris()

#Attribute: ['DESCR', 'data', 'feature_names', 'target', 'target_names']
print(DATA.target)
print(type(DATA))
