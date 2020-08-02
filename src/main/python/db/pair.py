from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.main.phyton.db.base import Base


class Pair(Base):
    __tablename__ = 'pair'

    id = Column(Integer, primary_key=True)
    primary_coin_id = Column(Integer, ForeignKey('coin.id'))
    secondary_coin_id = Column(Integer, ForeignKey('coin.id'))
    primary_coin = relationship("Coin", foreign_keys=[primary_coin_id])
    secondary_coin = relationship("Coin", foreign_keys=[secondary_coin_id])

    def __init__(self, primary_coin, secondary_coin):
        self.primary_coin = primary_coin
        self.secondary_coin = secondary_coin

    def __str__(self):
        return f'{self.secondary_coin.name}/{self.primary_coin.name}'
