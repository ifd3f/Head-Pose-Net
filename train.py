import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

import model


EPOCHS = 1000

inputs = pd.read_csv('ml_inputs.csv', index_col=0).astype(np.float32)
outputs = pd.read_csv('ml_outputs.csv', index_col=0).astype(np.float32)
X_train, X_test, y_train, y_test = train_test_split(inputs, outputs, shuffle=True)


with tf.Session() as sess:
    tf.keras.backend.set_session(sess)
    posenet = model.create_model()
    loss = tf.losses.mean_squared_error(labels=y_train, predictions=posenet(X_train))
    optimizer = tf.train.AdamOptimizer(0.01)
    train = optimizer.minimize(loss)

    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=25)
    posenet.fit(
        X_train, y_train,
        epochs=EPOCHS, 
        validation_split=0.2,
        batch_size=100, 
        callbacks=[early_stop])
    
    try:
        os.makedirs('./saved_models')
    except FileExistsError:
        pass
    tf.contrib.saved_model.save_keras_model(posenet, './saved_models')
