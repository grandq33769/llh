'''
Created on 2017年5月17日

@author: LokHim
'''
import os
import glob
import numpy as np
import keras
from PIL import Image
from itertools import product
from llh.Python.keras.face_regonition.input.input_name import URLBASE

def to_rgb(image):
    '''
    We can use the same array 3 times, converting to uint8 first
    This explicitly converts to np.uint8 once and is short
    '''
    return np.dstack([image.astype(np.uint8)] * 3)

def transform(image, shape):
    '''A function for transform an image to specific shape'''
    im_arr = np.array(image.resize((shape[0],shape[1]),Image.ANTIALIAS))
    try:
        arr = np.reshape(im_arr, shape)
    except ValueError:
        arr = np.reshape(to_rgb(im_arr), shape)
    return arr

def all_data(size,net):
    MODE_LIST = ('Training', 'Testing')
    CLASS_LIST = ('Positive', 'Negative')
    DATA_SIZE_LIST = []
    for path in product(MODE_LIST,CLASS_LIST):
        com_path = '/'+path[0]+'/'+net+'/'+path[1]+'/'
        DATA_SIZE_LIST.append(len([f for f in os.listdir(URLBASE+com_path)\
                              if os.path.isfile(os.path.join(URLBASE+com_path, f))]))
    TRAINING_SIZE = DATA_SIZE_LIST[0] + DATA_SIZE_LIST[1]
    TESTING_SIZE = DATA_SIZE_LIST[2] + DATA_SIZE_LIST[3]
    
    X_TRAIN = np.empty(shape=(TRAINING_SIZE, size, size, 3))
    X_TEST = np.empty(shape=(TESTING_SIZE, size, size, 3))
    Y_TRAIN = np.empty(shape=(TRAINING_SIZE, 1))
    Y_TEST = np.empty(shape=(TESTING_SIZE, 1))
    
    FINAL_LIST = [X_TRAIN, X_TEST]
    TARGET_LIST = [Y_TRAIN, Y_TEST]
    
    for mode, x, y in zip(MODE_LIST, FINAL_LIST, TARGET_LIST):
        print(mode, '...')
        index = 0
        for cla in CLASS_LIST:
            print(cla, '...')
            path = URLBASE + '/' + mode + '/' + cla + '/' + '*.jpg'
            for filename in glob.glob(path):
                with Image.open(filename, 'r') as img:
                    print(index)
                    x[index] = transform(img, (size, size, 3))
                    if cla == 'Positive':
                        y[index] = 1
                    else:
                        y[index] = 0
    
                    index += 1
    
    print('x_train:', X_TRAIN.size, 'y_train: ', Y_TRAIN.size)
    print('x_test:', X_TEST.size, 'y_test: ', Y_TEST.size)
    X_TRAIN = X_TRAIN.astype('float32')
    X_TEST = X_TEST.astype('float32')
    X_TRAIN /= 255
    X_TEST /= 255
    
    print('x_train shape:', X_TRAIN.shape)
    print(X_TRAIN.shape[0], 'train samples')
    print(X_TEST.shape[0], 'test samples')
    
    Y_TRAIN = keras.utils.to_categorical(Y_TRAIN, 2)
    Y_TEST = keras.utils.to_categorical(Y_TEST, 2)
    return X_TRAIN,Y_TRAIN,X_TEST,Y_TEST
