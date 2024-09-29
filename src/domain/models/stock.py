from sqlalchemy import Column, String, Float, DateTime
from src.infrastructure.db.db_setup import Base
from sqlalchemy.ext.declarative import declarative_base
class Stock(Base):
    __tablename__ = 'stocks'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)
    sector = Column(String)
    close_price = Column(Float)
    date = Column(DateTime)
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)

    def __init__(self, ticker, name, industry, sector, close_price, date, open=None, high=None, low=None, close=None, volume=None):
        self.ticker = ticker
        self.name = name
        self.industry = industry
        self.sector = sector
        self.close_price = close_price
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume