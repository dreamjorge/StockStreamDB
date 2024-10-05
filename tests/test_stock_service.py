# tests/test_stock_service.py
import pytest
from unittest.mock import MagicMock
from src.use_cases.stock_service import StockService
from src.domain.models.stock import Stock

@pytest.fixture
def mock_stock_repository():
    return MagicMock()

@pytest.fixture
def mock_stock_fetcher():
    return MagicMock()

@pytest.fixture
def stock_service(mock_stock_repository, mock_stock_fetcher):
    return StockService(stock_repository=mock_stock_repository, stock_fetcher=mock_stock_fetcher)

def test_fetch_existing_stock(stock_service, mock_stock_repository):
    # Arrange
    existing_stock = Stock(ticker="AAPL", name="Apple Inc.", industry="Technology", sector="Consumer Electronics", close=150.0, date="2024-01-01")
    mock_stock_repository.get_stock.return_value = existing_stock

    # Act
    stock = stock_service.fetch_stock("AAPL")

    # Assert
    assert stock == existing_stock
    mock_stock_repository.get_stock.assert_called_once_with("AAPL")
    mock_stock_repository.create_stock.assert_not_called()

def test_fetch_new_stock(stock_service, mock_stock_repository, mock_stock_fetcher):
    # Arrange
    mock_stock_repository.get_stock.return_value = None
    stock_data = {
        'ticker': 'AAPL',
        'name': 'Apple Inc.',
        'industry': 'Technology',
        'sector': 'Consumer Electronics',
        'close': 150.0,
        'date': '2024-01-01'
    }
    mock_stock_fetcher.fetch.return_value = stock_data

    # Act
    stock = stock_service.fetch_stock("AAPL")

    # Assert
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.industry == "Technology"
    assert stock.sector == "Consumer Electronics"
    assert stock.close == 150.0
    assert stock.date == "2024-01-01"

    mock_stock_repository.get_stock.assert_called_once_with("AAPL")
    mock_stock_fetcher.fetch.assert_called_once_with("AAPL")
    mock_stock_repository.create_stock.assert_called_once_with(stock)
