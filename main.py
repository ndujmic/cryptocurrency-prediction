import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import requests
import csv
import json
import tensorflow as tf

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
    current_data = []
    for i, data_point in enumerate(data):
        if i >= len(data) - 1:
            break
        current_data.append(data_point)
        if i != 0 and i % SET_NUM == 0:
            temp_data.append(current_data)
            current_data = []
    stop_point = int(len(temp_data) * 0.7)
    return temp_data[:stop_point], temp_data[stop_point+1:]


if __name__ == '__main__':

    data_endpoint = get_data()
    data_endpoint['time'] = pd.to_datetime(data_endpoint['time'], unit='s')

    test_data, train_data = split_data_train_test(data_endpoint['high'])

    # visual_data = data_endpoint.plot(kind="line", x='time', y='high')
    plt.plot(data_endpoint['time'], data_endpoint['high'], data_endpoint['time'], data_endpoint['low'])
    plt.show()


