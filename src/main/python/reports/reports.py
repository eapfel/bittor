import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.main.python.api.exmo_api import ExmoApi
from src.main.python.lstm.predict.lstm_predict import LSTMPredict

plt.style.use('fivethirtyeight')

api = ExmoApi()
lstm_predict = LSTMPredict(api)

df = lstm_predict.predict()

plt.figure(figsize=(16, 8))
plt.xlabel('Date')
plt.ylabel('Close')
plt.plot(df['Close'], 'b', label='Close Price')
plt.plot(df['Predictions'], 'r', label='Prediction')
plt.legend(loc='upper left', shadow=True, fontsize='x-large')


def ratios(x, y, z):
    predictions = list(df['Predictions'])[:-1]
    price = list(df['Close'])[:-1]
    corrects = []
    for i in range(len(predictions) - y, len(predictions) - z):
        if (predictions[i] * (1.0 + (x / 100.0))) > price[i] > (predictions[i] * (1.0 - (x / 100.0))):
            corrects.append(1.0)
        else:
            corrects.append(0.0)
    return np.average(corrects) * 100


def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


MAPE = [mape(df['Close'][-500:], df['Predictions'][-500:]),
        mape(df['Close'][-1000:-500], df['Predictions'][-1000:-500]),
        mape(df['Close'][-1500:-1000], df['Predictions'][-1500:-1000]),
        mape(df['Close'][-2000:-1500], df['Predictions'][-2000:-1500])]

Col1 = [ratios(15, i, i - 500) for i in range(500, 2001, 500)]
Col2 = [ratios(10, i, i - 500) for i in range(500, 2001, 500)]
Col3 = [ratios(5, i, i - 500) for i in range(500, 2001, 500)]

print(pd.DataFrame([MAPE, Col1, Col2, Col3],
                   index=["Mape", "Ratio 15%", "Ratio 10%", "Ratio 5%"],
                   columns=['0-500', "500-1000", "1000-1500", "1500-2000"]))
