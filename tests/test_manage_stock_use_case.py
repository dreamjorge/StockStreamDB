#test_manage_stock_use_case.py
import pytest
from unittest.mock import Mock
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.domain.models.stock import Stock
from datetime import datetime

@pytest.fixture
def mock_stock_repository():
    return Mock()

@pytest.fixture
def stock_use_case(mock_stock_repository):
    return ManageStockUseCase(mock_stock_repository)

def test_create_stock(stock_use_case, mock_stock_repository):
    stock = stock_use_case.create_stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close_price=150.0,
        date=datetime(2023, 9, 1)
    )
    assert stock.ticker == "AAPL"


def test_get_stock(stock_use_case, mock_stock_repository):
    stock = Stock(ticker="AAPL", name="Apple Inc.", industry="Technology", sector="Consumer Electronics", close_price=150.0, date=datetime(2023, 9, 1))

    # Configure the mock to return the expected stock
    mock_stock_repository.get_stock_by_ticker.return_value = stock

    # Call the use case method
    result = stock_use_case.get_stock("AAPL")

    # Check if the result matches the expected stock
    assert result == stock


def test_update_stock(stock_use_case, mock_stock_repository):
    stock = Stock(ticker="AAPL", name="Apple Inc.", industry="Technology", sector="Consumer Electronics", close_price=150.0, date=datetime(2023, 9, 1))
    mock_stock_repository.get_stock_by_ticker.return_value = stock

    updated_stock = stock_use_case.update_stock(ticker="AAPL", close_price=160.0)
    
    assert updated_stock.close_price == pytest.approx(160.0)
    mock_stock_repository.update.assert_called_once_with(stock)


def test_delete_stock(stock_use_case, mock_stock_repository):
    # Configure the mock to return a stock when querying by ticker
    mock_stock_repository.get_stock_by_ticker.return_value = Stock(ticker="AAPL", name="Apple Inc.", industry="Technology", sector="Consumer Electronics", close_price=150.0, date=datetime(2023, 9, 1))

    # Ensure delete is called
    mock_stock_repository.delete.return_value = True

    # Call the delete method in the use case
    result = stock_use_case.delete_stock("AAPL")

    # Assert the stock was successfully deleted
    assert result is True

    # Verify that delete was called once with the correct ticker
    mock_stock_repository.delete.assert_called_once_with("AAPL")

