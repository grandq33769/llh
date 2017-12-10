'''
Script for plotting result of mushroom_exp
Date: 2017/12/09
'''
import matplotlib.pyplot as plt
import numpy as np

CLF = ['Golden Classifier','Decision Tree','Random Forest']

FIG = plt.figure(1)

ATTR = np.linspace(22,15,8)
SIZE = np.linspace(70, 10, 7)

RESULT_A = [[0.43,0.43,0.43,0.43,0.7,0.8,0.18,0.2],
			[0.98,0.98,0.98,0.98,0.75,0.92,0.76,0.84],
			[0.98,0.98,0.98,0.98,0.75,0.97,0.89,0.9]]

RESULT_S = [[0.43,0.43,0.44,0.42,0.39,0.36,0.34],
			[0.98,0.98,0.79,0.7,0.59,0.32,0.37],
			[0.98,0.99,0.95,0.55,0.59,0.32,0.37]]

for y,l in zip(RESULT_A,CLF):
	plt.plot(ATTR,y,label=l)

plt.legend()
plt.xlabel('# of features')
plt.ylabel('Macro F1 score')
plt.title('Macro F1 score V.S # of features')

plt.show()

FIG2 = plt.figure(2)
for y,l in zip(RESULT_S,CLF):
	plt.plot(SIZE,y,label=l)

plt.legend()
plt.xlabel('Data size(%)')
plt.ylabel('Macro F1 score')
plt.title('Macro F1 score V.S data size')

plt.show()
