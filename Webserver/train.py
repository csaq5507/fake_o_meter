# First we import the required libraries
import os
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

from tensorflow.keras import backend as K

K.clear_session()

# Check tensorflow version
if float(tf.__version__[0]) < 2.0:
    print('Need to update tensorflow')
    exit()
else:
    print('Correct version of Tensorflow installed.')

# read training data
df = pd.read_csv('training_data/train.csv')
df = df.fillna(' ')
df.count()

tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['text'])
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

word_index = tokenizer.word_index
vocab_size = len(word_index)
print(vocab_size)

# Padding data
sequences = tokenizer.texts_to_sequences(df['text'])
padded = pad_sequences(sequences, maxlen=500, padding='post', truncating='post')

split = 0.2
split_n = int(round(len(padded) * (1 - split), 0))

train_data = padded[:split_n]
train_labels = df['label'].values[:split_n]
test_data = padded[split_n:]
test_labels = df['label'].values[split_n:]

# Global Vectors for Word Representation
embeddings_index = {}
with open('tmp/glove.6B.100d.txt') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
print(len(coefs))

embeddings_matrix = np.zeros((vocab_size + 1, 100))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embeddings_matrix[i] = embedding_vector

# create Model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size + 1, 100, weights=[embeddings_matrix], trainable=False),
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

# Create a callback that saves the model's weights
checkpoint_path = "training_weights/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# https://youtu.be/mw2kKyJu9gY?t=130
history = model.fit(train_data, train_labels, epochs=5, batch_size=100, validation_data=[test_data, test_labels], callbacks=[cp_callback])

print("Training Complete")
