'''
Created on 2017年5月17日

@author: LokHim
'''
import glob
import numpy as np
from PIL import Image
from llh.Python.keras.face_regonition.input.input_name import URLBASE


def to_rgb(image):
    '''
    We can use the same array 3 times, converting to uint8 first
    This explicitly converts to np.uint8 once and is short
    '''
    return np.dstack([image.astype(np.uint8)] * 3)


TRAINING_SIZE = 10000
TESTING_SIZE = 2000
MODE_LIST = ('Training', 'Testing')
CLASS_LIST = ('Positive', 'Negative')
SIZE_LIST = (TRAINING_SIZE, TESTING_SIZE)

X_TRAIN = np.empty(shape=(TRAINING_SIZE, 12, 12, 3))
X_TEST = np.empty(shape=(TESTING_SIZE, 12, 12, 3))
Y_TRAIN = np.empty(shape=(TRAINING_SIZE, 1))
Y_TEST = np.empty(shape=(TESTING_SIZE, 1))

FINAL_LIST = [X_TRAIN, X_TEST]
TARGET_LIST = [Y_TRAIN, Y_TEST]


def transform(image, shape):
    '''A function for transform an image to specific shape'''
    im_arr = np.array(image)
    try:
        arr = np.reshape(im_arr, shape)
    except ValueError:
        arr = np.reshape(to_rgb(im_arr), shape)
    return arr


for mode, x, y in zip(MODE_LIST, FINAL_LIST, TARGET_LIST):
    print(mode, '...')
    index = 0
    for cla in CLASS_LIST:
        print(cla, '...')
        path = URLBASE + '/' + mode + '/' + cla + '/' + '*.jpg'
        for filename in glob.glob(path):
            with Image.open(filename, 'r') as img:
                x[index] = transform(img, (12, 12, 3))
                if cla == 'Positive':
                    y[index] = 1
                else:
                    y[index] = 0

                index += 1

print('x_train:', X_TRAIN.size, 'y_train: ', Y_TRAIN.size)
print('x_test:', X_TEST.size, 'y_test: ', Y_TEST.size)
