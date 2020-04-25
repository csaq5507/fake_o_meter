# First we import the required libraries
import os
import tensorflow as tf
import numpy as np
import pandas as pd
import io
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers


from tensorflow.keras import backend as K
K.clear_session()


def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Conv1D(64, 5, activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=4),
        tf.keras.layers.LSTM(20, return_sequences=True),
        tf.keras.layers.LSTM(20),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(512),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(256),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    checkpoint_path = "training_weights/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    model.load_weights(latest)
    return model

def detect(data):
    # Create a new model instance
    model = create_model()
    data = np.array([data])
    result = model.predict(data)