from sqlalchemy import Column, String, Float, DateTime, Integer, UniqueConstraint
from src.infrastructure.db.db_setup import Base

class Stock(Base):
    __tablename__ = 'stocks'
    __table_args__ = (
        UniqueConstraint('ticker', 'date', name='uix_ticker_date'),  # Ensure ticker and date combination is unique
        {'extend_existing': True}
    )
    id = Column(Integer, primary_key=True, autoincrement=True)  # Enable autoincrement for id
    ticker = Column(String, nullable=False)  # Remove primary_key=True from ticker
    name = Column(String)
    industry = Column(String)
    sector = Column(String)
    date = Column(DateTime)
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)

    def __init__(self, ticker, name, industry, sector, date, open=None, high=None, low=None, close=None, volume=None):
        self.ticker = ticker
        self.name = name
        self.industry = industry
        self.sector = sector
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
