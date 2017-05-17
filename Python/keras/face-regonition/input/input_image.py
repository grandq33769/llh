'''
Created on 2017年5月17日

@author: LokHim
'''
import sys
import numpy as np
import glob
from PIL import Image
from input_name import URLBASE

def to_rgb(im):
    # we can use the same array 3 times, converting to
    # uint8 first
    # this explicitly converts to np.uint8 once and is short
    return np.dstack([im.astype(np.uint8)] * 3)

TRAINING_SIZE = 10000
TESTING_SIZE = 2000
MODE_LIST = ('Training','Testing')
CLASS_LIST = ('Positive','Negative')
SIZE_LIST = (TRAINING_SIZE,TESTING_SIZE)

x_train = np.empty(shape = (TRAINING_SIZE,12,12,3))
x_test = np.empty(shape = (TESTING_SIZE,12,12,3))
y_train = np.empty(shape = (TRAINING_SIZE,1))
y_test = np.empty(shape = (TESTING_SIZE,1))

FINAL_LIST = [x_train,x_test]
TARGET_LIST = [y_train,y_test]

for mode,x,y in zip(MODE_LIST,FINAL_LIST,TARGET_LIST):
    print(mode,'...')
    index = 0
    for cla in CLASS_LIST:
        print(cla,'...')
        path = URLBASE + '/' + mode + '/' + cla + '/' + '*.jpg'
        for filename in glob.glob(path):
            with Image.open(filename, 'r') as image:
                im_arr = np.array(image)
                try:
                    arr = np.reshape(im_arr, (12,12,3))
                except ValueError:
                    arr = np.reshape(to_rgb(im_arr), (12,12,3))
                x[index] = arr
                if cla == 'Positive':
                    y[index] = 1
                else:
                    y[index] = 0
                
                index += 1
                
print('x_train:',x_train.size,'y_train: ',y_train.size)
print('x_test:',x_test.size,'y_test: ',y_test.size)