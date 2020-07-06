from abc import ABC, abstractmethod
from string import Template

from src.main.python.config.config import Config


class BitcoinApi(ABC):
    market_name = None
    api_key = None
    secret = None
    password = None
    uid = None
    exchange = None
    can_short = None
    spread_target = None

    def __init__(self, market_name):
        self.market_name = market_name
        self.config = Config().get('markets').get(market_name)
        self.api_key = self.config.get('api_key')
        self.secret = self.config.get('secret')
        self.password = self.config.get('password')
        self.uid = self.config.get('uid')
        self.history_url = Template(self.config.get('history'))
        self.create_market_api()

    @abstractmethod
    def create_market_api(self):
        pass

    @abstractmethod
    def data_normalize(self, data):
        pass

    @abstractmethod
    def get_data_frame_history(self, data):
        pass

    def fetch_ticker(self):
        ticker = self.exchange.fetch_ticker('BTC/USD')

        return ticker

    def get_fees(self):
        return self.exchange.fetch_fees()

    def order_buy(self, volume):
        pass

    def order_sell(self, volume):
        pass
