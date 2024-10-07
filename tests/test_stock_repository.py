import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.domain.models.stock import Stock
from src.interfaces.common.enums import Granularity
from src.repositories.stock_repository import StockRepository
from typing import List


# Concrete implementation for testing
class ConcreteStockRepository(StockRepository):
    def create_stock(self, stock: Stock) -> Stock:
        pass

    def get(self, ticker: str) -> Stock:
        pass

    def update(self, stock: Stock) -> Stock:
        pass

    def delete_stock(self, ticker: str) -> bool:
        pass

    def save(self, stock):
        pass

    def get_stock_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        granularity: Granularity,
    ) -> List[Stock]:
        pass


@pytest.fixture
def mock_stock():
    return Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close=150.0,
        date=datetime(2024, 1, 1),
    )


@pytest.fixture
def stock_repository():
    return ConcreteStockRepository()


# Test for create_stock method
def test_create_stock(stock_repository, mock_stock):
    stock_repository.create_stock = MagicMock(return_value=mock_stock)
    stock = stock_repository.create_stock(mock_stock)
    assert stock == mock_stock
    stock_repository.create_stock.assert_called_once_with(mock_stock)


# Test for get method
def test_get_stock(stock_repository, mock_stock):
    stock_repository.get = MagicMock(return_value=mock_stock)
    stock = stock_repository.get("AAPL")
    assert stock == mock_stock
    stock_repository.get.assert_called_once_with("AAPL")


# Test for get method returning None when stock is not found
def test_get_stock_not_found(stock_repository):
    stock_repository.get = MagicMock(return_value=None)
    stock = stock_repository.get("MSFT")
    assert stock is None
    stock_repository.get.assert_called_once_with("MSFT")


# Test for update_stock method
def test_update_stock(stock_repository, mock_stock):
    updated_stock = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close=155.0,
        date=datetime(2024, 1, 1),
    )
    stock_repository.update = MagicMock(return_value=updated_stock)
    stock = stock_repository.update(updated_stock)
    assert stock.close == pytest.approx(
        155.0, rel=1e-9
    ), "Close price should be approximately 155.0"
    stock_repository.update.assert_called_once_with(updated_stock)


# Test for delete_stock method
def test_delete_stock(stock_repository):
    stock_repository.delete_stock = MagicMock(return_value=True)
    result = stock_repository.delete_stock("AAPL")
    assert result is True
    stock_repository.delete_stock.assert_called_once_with("AAPL")


# Test delete_stock method when the stock does not exist
def test_delete_stock_not_found(stock_repository):
    stock_repository.delete_stock = MagicMock(return_value=False)
    result = stock_repository.delete_stock("MSFT")
    assert result is False
    stock_repository.delete_stock.assert_called_once_with("MSFT")


# Test for save method
def test_save_stock(stock_repository, mock_stock):
    stock_repository.save = MagicMock()
    stock_repository.save(mock_stock)
    stock_repository.save.assert_called_once_with(mock_stock)


# Test for get_stock_data method
def test_get_stock_data(stock_repository, mock_stock):
    stock_data = [mock_stock]
    stock_repository.get_stock_data = MagicMock(return_value=stock_data)
    result = stock_repository.get_stock_data(
        "AAPL", datetime(2022, 1, 1), datetime(2023, 1, 1), Granularity.DAILY
    )
    assert result == stock_data
    stock_repository.get_stock_data.assert_called_once_with(
        "AAPL", datetime(2022, 1, 1), datetime(2023, 1, 1), Granularity.DAILY
    )


# Test get_stock_data method with empty result
def test_get_stock_data_empty(stock_repository):
    stock_repository.get_stock_data = MagicMock(return_value=[])
    result = stock_repository.get_stock_data(
        "AAPL", datetime(2022, 1, 1), datetime(2023, 1, 1), Granularity.DAILY
    )
    assert result == []
    stock_repository.get_stock_data.assert_called_once_with(
        "AAPL", datetime(2022, 1, 1), datetime(2023, 1, 1), Granularity.DAILY
    )


# Test for exception handling (you can mock exception handling in methods)
def test_get_stock_data_with_exception(stock_repository):
    stock_repository.get_stock_data = MagicMock(side_effect=Exception("Database error"))
    with pytest.raises(Exception, match="Database error"):
        stock_repository.get_stock_data(
            "AAPL", datetime(2022, 1, 1), datetime(2023, 1, 1), Granularity.DAILY
        )
