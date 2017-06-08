'''Neural network for calibration after 48-net'''

from llh.Python.keras.face_regonition.model import *

MODEL = Sequential()

MODEL.add(Conv2D(64, (5, 5), padding='same',
                 input_shape=X_TRAIN.shape[1:]))
MODEL.add(Activation('relu'))
MODEL.add(MaxPooling2D(pool_size=(3, 3), strides=2))
# TODO: add normalization layer (9*9)
MODEL.add(Conv2D(64, (5, 5), padding='same',
                 input_shape=X_TRAIN.shape[1:]))
# TODO: add normalization layer (9*9)
MODEL.add(Flatten())
MODEL.add(Dense(256))
MODEL.add(Activation('tanh'))
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

MODEL.save('48-net-calibration.h5')
