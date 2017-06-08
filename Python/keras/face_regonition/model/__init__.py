from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from llh.Python.keras.face_regonition.input.input_image import X_TRAIN, Y_TRAIN, X_TEST, Y_TEST
__all__ = [BATCH_SIZE, NUM_CLASSES, EPOCHS, X_TRAIN, X_TEST, Y_TRAIN, Y_TEST]

BATCH_SIZE = 32
NUM_CLASSES = 2
EPOCHS = 200

X_TRAIN = X_TRAIN.astype('float32')
X_TEST = X_TEST.astype('float32')
X_TRAIN /= 255
X_TEST /= 255

print('x_train shape:', X_TRAIN.shape)
print(X_TRAIN.shape[0], 'train samples')
print(X_TEST.shape[0], 'test samples')

Y_TRAIN = keras.utils.to_categorical(Y_TRAIN, NUM_CLASSES)
Y_TEST = keras.utils.to_categorical(Y_TEST, NUM_CLASSES)
