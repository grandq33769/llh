from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from llh.Python.keras.face_regonition.input.input_image import all_data


BATCH_SIZE = 256
NUM_CLASSES = 2
EPOCHS = 100

__all__ = ['BATCH_SIZE', 'NUM_CLASSES', 'EPOCHS','Sequential',\
           'Dense', 'Activation', 'Flatten','Conv2D', 'MaxPooling2D',\
           'all_data','keras']
