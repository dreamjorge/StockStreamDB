# tests/test_stock_service.py
import pytest
from unittest.mock import MagicMock
from src.use_cases.stock_service import StockService
from src.domain.models.stock import Stock

# from domain.models.stock import Stock


@pytest.fixture
def mock_stock_repository():
    return MagicMock()


@pytest.fixture
def mock_stock_fetcher():
    return MagicMock()


@pytest.fixture
def stock_service(mock_stock_repository, mock_stock_fetcher):
    return StockService(
        stock_repository=mock_stock_repository, stock_fetcher=mock_stock_fetcher
    )


def test_fetch_existing_clear(stock_service, mock_stock_repository):
    # Arrange
    existing_stock = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close=150.0,
        date="2024-01-01",
    )
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
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "industry": "Technology",
        "sector": "Consumer Electronics",
        "close": 150.0,
        "date": "2024-01-01",
    }
    mock_stock_fetcher.fetch.return_value = stock_data

    # Act
    stock = stock_service.fetch_stock("AAPL")

    # Assert
    assert isinstance(stock, Stock)  # Assert the returned object is of type Stock
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.close == pytest.approx(
        150.0, rel=1e-9
    ), "Close price should be approximately 155.0"
    assert stock.date == "2024-01-01"

    mock_stock_repository.get_stock.assert_called_once_with("AAPL")
    mock_stock_fetcher.fetch.assert_called_once_with("AAPL")
    mock_stock_repository.create_stock.assert_called_once_with(stock)


def test_fetch_stock_fetcher_failure(
    stock_service, mock_stock_repository, mock_stock_fetcher
):
    # Arrange
    mock_stock_repository.get_stock.return_value = None
    mock_stock_fetcher.fetch.side_effect = Exception("Fetcher failed")

    # Act / Assert
    with pytest.raises(Exception, match="Fetcher failed"):
        stock_service.fetch_stock("INVALID_TICKER")
    mock_stock_repository.get_stock.assert_called_once_with("INVALID_TICKER")
    mock_stock_fetcher.fetch.assert_called_once_with("INVALID_TICKER")


def test_fetch_empty_ticker(stock_service, mock_stock_repository, mock_stock_fetcher):
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="Ticker cannot be empty"):
        stock_service.fetch_stock("")


def test_fetch_none_ticker(stock_service, mock_stock_repository, mock_stock_fetcher):
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="Ticker cannot be None"):
        stock_service.fetch_stock(None)


def test_fetch_incomplete_stock_data(
    stock_service, mock_stock_repository, mock_stock_fetcher
):
    # Arrange
    mock_stock_repository.get_stock.return_value = None
    stock_data = {
        "ticker": "AAPL",
        "name": None,  # Name is missing
        "industry": "Technology",
        "sector": "Consumer Electronics",
        "close": 150.0,
        "date": "2024-01-01",
    }
    mock_stock_fetcher.fetch.return_value = stock_data

    # Act
    stock = stock_service.fetch_stock("AAPL")

    # Assert
    assert stock.name is None
    assert stock.ticker == "AAPL"
    mock_stock_fetcher.fetch.assert_called_once_with("AAPL")


def test_add_stock(stock_service, mock_stock_repository):
    # Arrange
    stock = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close=150.0,
        date="2024-01-01",
    )
    mock_stock_repository.create_stock.return_value = True

    # Act
    result = stock_service.add_stock(stock)

    # Assert
    assert result is True
    mock_stock_repository.create_stock.assert_called_once_with(stock)


def test_remove_stock(stock_service, mock_stock_repository):
    # Arrange
    ticker = "AAPL"
    mock_stock_repository.delete_stock.return_value = True
    # Act
    result = stock_service.remove_stock(ticker)

    # Assert
    assert result is True
    mock_stock_repository.delete_stock.assert_called_once_with(ticker)
