'''
Created on 2017年4月27日

@author: LokHim
'''
import numpy as np
from sklearn.decomposition import PCA
import random as r
import Input
import Plot

di = Input.DataInputter('D:/Ecllipse/my-code/Python/keras/nn-compare/mnist-data')
images, labels = di.get_testing_data_and_labels()
ran_list = []
images_list = []
num_of_pt = 5000

print('Randoming...')
for num in range(0,num_of_pt):
    ran = r.randint(0,len(images)-1)
    ran_list.append(ran)
    images_list.append(images[ran])

print('PCA...')
pca = PCA(n_components=2)
transform = pca.fit(images_list).transform(images_list)

print('Ploting...')
Plot.plot(transform,labels,ran_list)