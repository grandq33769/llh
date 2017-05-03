'''
Created on 2017年4月27日

@author: LokHim
'''

import keras
import Plot
import random as r
from keras.datasets import mnist
from keras.models import load_model
from keras.models import Model
from sklearn.decomposition import PCA

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_train = x_train.astype('float32')
x_train /= 255
print(x_train.shape[0], 'train samples')

model = load_model('DNN_2.h5')

intermediate_layer_model = Model(inputs=model.input,
                                 outputs=model.get_layer(index = 4).output)
sample = x_train[0].reshape(1,784)
intermediate_output = intermediate_layer_model.predict(x_train)

pca = PCA(n_components=2)
transfrom = pca.fit(intermediate_output).transform(intermediate_output)

ran_list = []
images_list = []
num_of_pt = 5000
for num in range(0,num_of_pt):
    ran = r.randint(0,len(transfrom)-1)
    ran_list.append(ran)
    images_list.append(transfrom[ran])
    
print(images_list[0])
Plot.plot(images_list,y_train,ran_list)