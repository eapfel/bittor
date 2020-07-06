import json

import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM, Activation
from keras.models import Sequential

from src.main.python.api.bitcoin_api import BitcoinApi
from src.main.python.lstm.bittor_lstm import BittorLSTM
from src.main.python.utils.utils import base_dir


# noinspection PyMethodMayBeStatic
class LSTMTraining(BittorLSTM):

    def __init__(self, api: BitcoinApi):
        super().__init__(api)

    def fit(self):
        df = self.get_data_frame()
        x, y = self.__create_x_and_y(df)
        model = self.__create_model(x, y)
        nn = self.__train_model(model, x, y)
        self.__save(nn, model)

        return df, x, y

    def __create_x_and_y(self, df):
        data = np.asarray(df['Close'])
        data = np.atleast_2d(data)
        data = data.T

        x = np.atleast_3d(
            np.array([data[start:start + self.OBS] for start in range(0, data.shape[0] - self.OBS)]))
        y = data[self.OBS:]

        return x, y

    def __create_model(self, x, y):
        model = Sequential()
        model.add(LSTM(input_shape=(x.shape[1], 1), units=15, return_sequences=True))
        model.add(LSTM(input_shape=(y.shape[1], 1), units=15, return_sequences=False))
        model.add(Dense(1))
        model.add(Activation('linear'))
        model.compile(loss="mape", optimizer="rmsprop")

        return model

    def __train_model(self, model, x, y):
        return model.fit(x, y, epochs=200, batch_size=50, verbose=2, shuffle=True)

    def __save(self, nn, model):
        data_dir = base_dir() / 'data'

        pd.DataFrame(nn.history).to_csv(data_dir / self.LOSS_FILE_NAME)
        model_params = json.dumps(nn.params)
        with open(data_dir / self.NOMINAL_PARAMS_FILE_NAME, "w") as json_file:
            json_file.write(model_params)

        model_json = model.to_json()
        with open(data_dir / self.NOMINAL_FILE_NAME, "w") as json_file:
            json_file.write(model_json)

        model.save_weights(str(data_dir / self.NOMINAL_WEIGHT_FILE_NAME))
