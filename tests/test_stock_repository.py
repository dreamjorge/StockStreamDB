import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository
from typing import List, Optional


# Concrete implementation for testing
class ConcreteStockRepository(StockRepository):
    def add(self, stock: Stock) -> Stock:
        pass

    def get_by_ticker(self, ticker: str) -> Optional[Stock]:
        pass

    def get_all(self) -> List[Stock]:
        pass

    def update(self, stock: Stock) -> Stock:
        pass

    def delete(self, ticker: str) -> None:
        pass


@pytest.fixture
def mock_stock():
    return Stock(
        id=1,
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 1, 1),
        close=150.0,
    )


@pytest.fixture
def stock_repository():
    return ConcreteStockRepository()


# Test for add method
def test_add_stock(stock_repository, mock_stock):
    stock_repository.add = MagicMock(return_value=mock_stock)
    stock = stock_repository.add(mock_stock)
    assert stock == mock_stock
    stock_repository.add.assert_called_once_with(mock_stock)


# Test for get_by_ticker method
def test_get_stock(stock_repository, mock_stock):
    stock_repository.get_by_ticker = MagicMock(return_value=mock_stock)
    stock = stock_repository.get_by_ticker("AAPL")
    assert stock == mock_stock
    stock_repository.get_by_ticker.assert_called_once_with("AAPL")


# Test for get_by_ticker method returning None when stock is not found
def test_get_stock_not_found(stock_repository):
    stock_repository.get_by_ticker = MagicMock(return_value=None)
    stock = stock_repository.get_by_ticker("MSFT")
    assert stock is None
    stock_repository.get_by_ticker.assert_called_once_with("MSFT")


# Test for update method
def test_update_stock(stock_repository, mock_stock):
    updated_stock = Stock(
        id=1,
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 1, 1),
        close=155.0,
    )
    stock_repository.update = MagicMock(return_value=updated_stock)
    stock = stock_repository.update(updated_stock)
    assert stock.close == pytest.approx(155.0, rel=1e-9)
    stock_repository.update.assert_called_once_with(updated_stock)


# Test for delete method
def test_delete_stock(stock_repository):
    stock_repository.delete = MagicMock(return_value=None)
    stock_repository.delete("AAPL")
    stock_repository.delete.assert_called_once_with("AAPL")