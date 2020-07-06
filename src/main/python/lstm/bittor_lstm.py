import random as rn

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

from src.main.python.api.bitcoin_api import BitcoinApi
from src.main.python.utils.utils import base_dir


# from typing import Final


# noinspection PyMethodMayBeStatic
class BittorLSTM:
    OBS = 20
    LOSS_FILE_NAME = 'BTC_nominal_loss.csv'
    NOMINAL_PARAMS_FILE_NAME = 'BTC_nominal_params.json'
    NOMINAL_FILE_NAME = 'BTC_nominal.json'
    NOMINAL_WEIGHT_FILE_NAME = 'BTC_nominal_weights.h5'
    sc = None

    def __init__(self, api: BitcoinApi):
        np.random.seed(1)
        tf.random.set_seed(1)
        rn.seed(1)
        self.api = api

    def get_data_frame(self):
        return self.__transform_two_dimensions(self.__get_data_normalize())

    def __get_data_normalize(self):
        return self.api.get_data_frame_history()

    def __transform_two_dimensions(self, df):
        self.sc = StandardScaler()
        df['Close'] = self.sc.fit_transform(df['Close'].values.reshape(-1, 1))

        return df

    def data_dir(self):
        return base_dir() / 'data'
