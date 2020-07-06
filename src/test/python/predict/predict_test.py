import unittest

from src.main.python.api.exmo_api import ExmoApi
from src.main.python.lstm.predict.lstm_predict import LSTMPredict


class PredictTest(unittest.TestCase):

    def test_predict(self):
        lstm_predict = LSTMPredict(ExmoApi())

        result = lstm_predict.predict()

        self.assertTrue(len(result) > 0)
