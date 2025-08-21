from sqlalchemy.orm import Session
from typing import List, Optional

from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository
from src.infrastructure.db.models import StockDB


def to_domain(stock_db: StockDB) -> Stock:
    """Converts a StockDB object to a Stock domain object."""
    return Stock(
        id=stock_db.id,
        ticker=stock_db.ticker,
        name=stock_db.name,
        industry=stock_db.industry,
        sector=stock_db.sector,
        date=stock_db.date,
        open=stock_db.open,
        high=stock_db.high,
        low=stock_db.low,
        close=stock_db.close,
        volume=stock_db.volume,
        market_cap=stock_db.market_cap,
        pe_ratio=stock_db.pe_ratio,
    )


def to_persistence(stock: Stock) -> StockDB:
    """Converts a Stock domain object to a StockDB object."""
    return StockDB(
        id=stock.id,
        ticker=stock.ticker,
        name=stock.name,
        industry=stock.industry,
        sector=stock.sector,
        date=stock.date,
        open=stock.open,
        high=stock.high,
        low=stock.low,
        close=stock.close,
        volume=stock.volume,
        market_cap=stock.market_cap,
        pe_ratio=stock.pe_ratio,
    )


class StockRepositoryImpl(StockRepository):
    """Implementation of the StockRepository using SQLAlchemy."""

    def __init__(self, session: Session):
        """Initialize the repository.

        Args:
            session: The SQLAlchemy session.
        """
        self.session = session

    def add(self, stock: Stock) -> Stock:
        """Add a stock to the repository.

        Args:
            stock: The stock to add.

        Returns:
            The added stock.
        """
        stock_db = to_persistence(stock)
        self.session.add(stock_db)
        self.session.commit()
        return to_domain(stock_db)

    def get_by_ticker(self, ticker: str) -> Optional[Stock]:
        """Get a stock by its ticker.

        Args:
            ticker: The stock ticker.

        Returns:
            The stock if found, otherwise None.
        """
        stock_db = self.session.query(StockDB).filter_by(ticker=ticker).first()
        return to_domain(stock_db) if stock_db else None

    def get_all(self) -> List[Stock]:
        """Get all stocks from the repository.

        Returns:
            A list of all stocks.
        """
        stocks_db = self.session.query(StockDB).all()
        return [to_domain(stock_db) for stock_db in stocks_db]

    def update(self, stock: Stock) -> Stock:
        """Update a stock in the repository.

        Args:
            stock: The stock to update.

        Returns:
            The updated stock.
        """
        stock_db = self.session.query(StockDB).filter_by(id=stock.id).first()
        if stock_db:
            stock_db.name = stock.name
            stock_db.industry = stock.industry
            stock_db.sector = stock.sector
            stock_db.date = stock.date
            stock_db.open = stock.open
            stock_db.high = stock.high
            stock_db.low = stock.low
            stock_db.close = stock.close
            stock_db.volume = stock.volume
            stock_db.market_cap = stock.market_cap
            stock_db.pe_ratio = stock.pe_ratio
            self.session.commit()
            return to_domain(stock_db)
        return None

    def delete(self, ticker: str) -> None:
        """Delete a stock from the repository.

        Args:
            ticker: The stock ticker.
        """
        stock_db = self.session.query(StockDB).filter_by(ticker=ticker).first()
        if stock_db:
            self.session.delete(stock_db)
            self.session.commit()
