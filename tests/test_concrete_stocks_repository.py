from unittest.mock import MagicMock
from src.domain.models.stock import Stock
from src.repositories.concrete_stocks_repository import ConcreteStocksRepository

def test_create_stock():
    session = MagicMock()
    repo = ConcreteStocksRepository(session)

    stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close_price=150.0, date="2023-01-01")
    repo.create_stock(stock)

    session.add.assert_called_once_with(stock)
    session.commit.assert_called_once()
