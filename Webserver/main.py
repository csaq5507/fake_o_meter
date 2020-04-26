from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import cgi
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import backend as K
import pickle

##
#
# You first need to train the model so a tokenizer.pickle(dictionary) & the trained weights get generated
#
##

# initialize neural network
K.clear_session()

# Running on a apache2 server, reverse proxy to this directory
hostName = "localhost"
serverPort = 8080

# Create a new model instance
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

vocab_size = len(tokenizer.word_index)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size + 1, 100),
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


# Neural network initialized

# NN detector

def detect(data):
    sequences = tokenizer.texts_to_sequences([data])
    padded = pad_sequences(sequences, maxlen=500, padding='post', truncating='post')
    data = np.array(padded)
    result = model.predict(data)
    return result[0][0]


# Webserver
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Why u do this?')

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        text = 0

        for field in form.keys():
            if field == "text":
                text = form[field]

        if text == 0:
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write("No text given")
            self.wfile.write(response.getvalue())
        else:
            self.send_response(200)
            self.end_headers()
            result = detect(text.value)
            self.wfile.write(str(result).encode("utf8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
