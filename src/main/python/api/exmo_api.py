import logging as log
from datetime import datetime, timedelta

import ccxt
from pandas import json_normalize
from pandas import read_json

from src.main.python.api.bitcoin_api import BitcoinApi


class ExmoApi(BitcoinApi):

    def __init__(self):
        super().__init__('exmo')

    def create_market_api(self):
        self.exchange = ccxt.exmo({
            'apiKey': self.api_key,
            'secret': self.secret
        })

    def get_data_frame_history(self):
        hours_since_today = self.config.get('hours_since_today')
        resolution = self.config.get('resolution')

        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        since = now - timedelta(hours=hours_since_today)
        since = since.replace(hour=0, minute=0, second=0, microsecond=0)

        log.info(f"get historical data from {since} to {now}")

        return self.data_normalize(
            read_json(
                self.history_url.substitute(r=resolution, f=int(datetime.timestamp(since)),
                                            t=int(datetime.timestamp(now)))))

    def data_normalize(self, data):
        df = json_normalize(data['candles'])
        df = df.rename(columns={'t': 'Date', 'o': 'Open', 'c': 'Close', 'h': 'High', 'l': 'Low', 'v': 'Volume'})
        df['Date'] = [datetime.fromtimestamp(x / 1000) for x in list(df['Date'])]
        df = df.sort_values(by='Date')
        df.index = df['Date']
        df = df.drop('Date', axis=1)

        return df
