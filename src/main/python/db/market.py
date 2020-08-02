from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from src.main.python.db.base import Base


class Market(Base):
    __tablename__ = 'market'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    wallet = relationship("Wallet", backref=backref("wallet"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name, active, wallet):
        self.name = name
        self.active = active
        self.wallet = wallet
