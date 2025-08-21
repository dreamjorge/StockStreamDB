# tests/test_stock_service.py
import pytest
from unittest.mock import MagicMock
from src.use_cases.stock_service import StockService
from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository
from src.infrastructure.fetchers.stock_fetcher import StockFetcher
from datetime import datetime


@pytest.fixture
def mock_stock_repository():
    return MagicMock(spec=StockRepository)


@pytest.fixture
def mock_stock_fetcher():
    return MagicMock(spec=StockFetcher)


@pytest.fixture
def stock_service(mock_stock_repository, mock_stock_fetcher):
    return StockService(
        stock_repository=mock_stock_repository, stock_fetcher=mock_stock_fetcher
    )


def test_fetch_existing_clear(stock_service, mock_stock_repository):
    # Arrange
    existing_stock = Stock(
        id=1,
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 1, 1),
        close=150.0,
    )
    mock_stock_repository.get_by_ticker.return_value = existing_stock

    # Act
    stock = stock_service.fetch_stock("AAPL")

    # Assert
    assert stock == existing_stock
    mock_stock_repository.get_by_ticker.assert_called_once_with("AAPL")
    mock_stock_repository.add.assert_not_called()


def test_fetch_new_stock(stock_service, mock_stock_repository, mock_stock_fetcher):
    # Arrange
    mock_stock_repository.get_by_ticker.return_value = None
    stock_data = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "industry": "Technology",
        "sector": "Consumer Electronics",
        "close": 150.0,
        "date": "2024-01-01",
    }
    mock_stock_fetcher.get_stock_data.return_value = stock_data

    # Act
    stock = stock_service.fetch_stock("AAPL")

    # Assert
    assert isinstance(stock, Stock)
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.close == pytest.approx(150.0, rel=1e-9)

    mock_stock_repository.get_by_ticker.assert_called_once_with("AAPL")
    mock_stock_fetcher.get_stock_data.assert_called_once_with("AAPL")
    mock_stock_repository.add.assert_called_once()


def test_add_stock(stock_service, mock_stock_repository):
    # Arrange
    stock = Stock(
        id=1,
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 1, 1),
        close=150.0,
    )
    mock_stock_repository.add.return_value = stock

    # Act
    result = stock_service.add_stock(stock)

    # Assert
    assert result == stock
    mock_stock_repository.add.assert_called_once_with(stock)


def test_remove_stock(stock_service, mock_stock_repository):
    # Arrange
    ticker = "AAPL"
    mock_stock_repository.delete.return_value = None
    # Act
    stock_service.remove_stock(ticker)

    # Assert
    mock_stock_repository.delete.assert_called_once_with(ticker)
