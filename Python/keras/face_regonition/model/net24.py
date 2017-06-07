'''
Created on 2017年6月7日

@author: LokHim
'''

from __future__ import print_function
import keras
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from llh.Python.keras.face_regonition.input.input_image import X_TRAIN, Y_TRAIN, X_TEST, Y_TEST

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

MODEL = Sequential()

MODEL.add(Conv2D(64, (5, 5), padding='same',
                 input_shape=X_TRAIN.shape[1:]))
MODEL.add(Activation('relu'))
MODEL.add(MaxPooling2D(pool_size=(3, 3), strides=2))
MODEL.add(Flatten())
MODEL.add(Dense(128))
MODEL.add(Activation('tanh'))
# Concatenate 12-net result
IMPORT_NET = load_model('12-net.h5')
NET12 = Model(inputs=IMPORT_NET.input,
              outputs=IMPORT_NET.get_layer(index=6).output)

MODEL.add(Dense(NUM_CLASSES))
MODEL.add(Activation('softmax'))

# initiate RMSprop optimizer
OPT = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

# Let's train the model using RMSprop
MODEL.compile(loss='categorical_crossentropy',
              optimizer=OPT,
              metrics=['accuracy'])


HISTORY = MODEL.fit(X_TRAIN, Y_TRAIN,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=(X_TEST, Y_TEST),
                    shuffle=True)

SCORE = MODEL.evaluate(X_TEST, Y_TEST, verbose=0)

print('Test loss:', SCORE[0])
print('Test accuracy:', SCORE[1])

MODEL.save('12-net.h5')
