from sqlalchemy import Column, String, Integer, Float, Date, BigInteger, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)
    sector = Column(String)
    close = Column(Float)
    market_cap = Column(Float)
    pe_ratio = Column(Float)


    prices = relationship("StockPrice", back_populates="stock")
    fundamentals = relationship("Fundamental", back_populates="stock")
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="stock")


class StockPrice(Base):
    __tablename__ = 'stock_prices'

    price_id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), ForeignKey('stocks.ticker'))
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)

    stock = relationship("Stock", back_populates="prices")


class Fundamental(Base):
    __tablename__ = 'fundamentals'

    fundamental_id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), ForeignKey('stocks.ticker'))
    date = Column(Date)
    pe_ratio = Column(Float)
    eps = Column(Float)
    market_cap = Column(BigInteger)
    revenue = Column(BigInteger)
    net_income = Column(BigInteger)
    total_assets = Column(BigInteger)

    stock = relationship("Stock", back_populates="fundamentals")


class SentimentAnalysis(Base):
    __tablename__ = 'sentiment_analysis'

    sentiment_id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), ForeignKey('stocks.ticker'))
    news_title = Column(Text)
    news_content = Column(Text)
    sentiment_score = Column(Float)
    date = Column(Date)

    stock = relationship("Stock", back_populates="sentiment_analysis")
