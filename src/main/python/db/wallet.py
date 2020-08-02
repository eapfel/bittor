from sqlalchemy import Column, Integer, DateTime, Numeric
from sqlalchemy.sql import func

from src.main.python.db.base import Base


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    usd = Column(Numeric)
    btc = Column(Numeric)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, usd, btc):
        self.usd = usd
        self.btc = btc
