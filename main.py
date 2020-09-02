import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

SET_NUM = 31


def get_data():
    endpoint = 'https://min-api.cryptocompare.com/data/histoday'
    res = requests.get(endpoint + '?fsym=BTC&tsym=USD&limit=2000')

    return pd.DataFrame(json.loads(res.content)['Data'])


def split_data_train_test(data):
    """"
        Return data in slices, each len == SET_NUM
        70% as test data, 30% as train data
    """
    temp_data = []
    for i, data_point in enumerate(data):
        if i < len(data) - SET_NUM:
            temp_data.append(data[i:i+SET_NUM].values)
    stop_point = int(len(temp_data) * 0.7)
    return temp_data[:stop_point], temp_data[stop_point+1:]


if __name__ == '__main__':

    data_endpoint = get_data()
    data_endpoint['time'] = pd.to_datetime(data_endpoint['time'], unit='s')

    train_data, test_data = split_data_train_test(data_endpoint['high'])

    x_train = np.array([x[:30] for x in train_data])
    x_train = x_train.reshape(x_train.shape + (1,))

    y_train = np.array([x[-1] for x in train_data])
    y_train = y_train.reshape(y_train.shape + (1,))

    x_test = np.array([x[:30] for x in test_data])
    x_test = x_test.reshape(x_test.shape + (1,))

    y_test = np.array([x[-1] for x in test_data])
    y_test = y_test.reshape(y_test.shape + (1,))

    # visual_data = data_endpoint.plot(kind="line", x='time', y='high')
    # plt.plot(data_endpoint['time'], data_endpoint['high'], data_endpoint['time'], data_endpoint['low'])
    # plt.show()

    #build model

    model = keras.Sequential()
    print(x_train.shape)
    layer = layers.LSTM(
        units=32,
        return_sequences=True,
        activation='relu',
        dropout=0.2
    )
    model.add(layer)

    model.add(layers.LSTM(
        units=32,
        return_sequences=True,
        activation='relu'))
    model.add(layers.LSTM(units=32))
    model.add(layers.Dense(units=1))

    model.compile(
        loss='msle',
        optimizer="adam",
        metrics=["accuracy"],
    )

    m = model.fit(
        x_train, y_train, validation_data=(x_test, y_test), epochs=5, batch_size=64
    )





