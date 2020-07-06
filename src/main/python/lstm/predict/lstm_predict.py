import numpy as np
from tensorflow.keras.models import model_from_json

from src.main.python.api.bitcoin_api import BitcoinApi
from src.main.python.lstm.bittor_lstm import BittorLSTM


class LSTMPredict(BittorLSTM):

    def __init__(self, api: BitcoinApi):
        super().__init__(api)

    def predict(self):
        df = self.get_data_frame()
        model = self.load_model()
        predictions = [model.predict(np.asarray(df['Close'])[i:i + self.OBS].reshape(1, self.OBS, 1)) for i in
                       range(len(df) - self.OBS)]
        predictions = [df['Close'].iloc[0]] * self.OBS + [val[0][0] for val in predictions]
        # predictions2 = [model.predict(np.asarray(df['Close'])[-self.OBS].reshape(1, self.OBS, 1))]
        df['Predictions'] = predictions
        df['Close'] = self.sc.inverse_transform(df['Close'])
        df['Predictions'] = self.sc.inverse_transform(df['Predictions'])

        return df

    def load_model(self):
        data_dir = self.data_dir()

        json_file = open(data_dir / self.NOMINAL_FILE_NAME)
        loaded_model_json = json_file.read()
        json_file.close()

        model = model_from_json(loaded_model_json)

        model.load_weights(str((data_dir / self.NOMINAL_WEIGHT_FILE_NAME)))

        return model
