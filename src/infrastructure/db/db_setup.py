from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    ticker = Column(String, primary_key=True)
    close_price = Column(Float)
    date = Column(DateTime)

def get_engine():
    return create_engine("sqlite:///src/infrastructure/db/database.db")

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
