import unittest

from src.main.python.api.exmo_api import ExmoApi
from src.main.python.lstm.training.lstm_training import LSTMTraining
from src.main.python.utils.utils import base_dir


class TrainingTest(unittest.TestCase):

    def test_path(self):
        path = base_dir()
        self.assertTrue(path.name == 'bittor')
        self.assertTrue((path / 'data').is_dir())

    def test_training(self):
        lstm_training = LSTMTraining(ExmoApi())

        df, x, y = lstm_training.fit()

        # self.assertEqual(2, df['Close'].ndim)
        self.assertTrue(len(x) == len(y))
