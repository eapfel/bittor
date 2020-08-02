from sqlalchemy import Column, Integer, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.main.python.db.base import Base


class Candle(Base):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('market.id'))
    market = relationship("Market", foreign_keys=[market_id])
    pair_id = Column(Integer, ForeignKey('pair.id'))
    pair = relationship("Pair", foreign_keys=[pair_id])
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    bid = Column(Numeric)
    ask = Column(Numeric)
    volume = Column(Numeric)
    volume_curr = Column(Numeric)
    time_created = Column(TIMESTAMP(timezone=True))
    time_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    def __init__(self, market, pair, bid, ask, open, close, high, low, volume, volume_curr):
        self.market = market
        self.pair = pair
        self.bid = bid
        self.ask = ask
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.volume_curr = volume_curr

    def __str__(self):
        return f"date:{self.time_created}, market:{self.market.name}, pair:{self.pair.__str__()}, open:{self.open} close:{self.close} high:{self.high}, low:{self.low}"
