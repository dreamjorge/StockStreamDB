import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.infrastructure.db.stock_repository import StockRepository
from requests.exceptions import RequestException
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.domain.models.stock import Stock


@pytest.fixture
def mock_db_session():
    return MagicMock()  # Mocking the database session


# Test for a successful connection and valid data
@patch("yfinance.Ticker")
def test_get_stock_data_success(mock_ticker):
    mock_history = MagicMock()
    mock_df = pd.DataFrame(
        {
            "Close": [150],
        },
        index=[pd.Timestamp("2023-09-01")],
    )  # Create a valid DataFrame with a 'Close' column

    mock_history.history.return_value = mock_df
    mock_ticker.return_value = mock_history

    stock_repo = StockRepository()
    stock_data = stock_repo.get_stock_data("AAPL", "1mo")

    assert stock_data is not None
    assert stock_data["close"] == 150
    assert stock_data["date"] == "2023-09-01"


# Test when no data is found (empty DataFrame)
@patch("yfinance.Ticker")
def test_get_stock_data_no_data(mock_ticker):
    mock_history = MagicMock()
    mock_df = pd.DataFrame()  # Empty DataFrame
    mock_history.history.return_value = mock_df
    mock_ticker.return_value = mock_history

    stock_repo = StockRepository()
    stock_data = stock_repo.get_stock_data("AAPL", "1mo")

    assert stock_data is None


# Test to simulate a connection error (RequestException)
@patch("yfinance.Ticker")
def test_get_stock_data_connection_error(mock_ticker):
    mock_history = MagicMock()
    mock_history.history.side_effect = RequestException("Connection error")
    mock_ticker.return_value = mock_history

    stock_repo = StockRepository()
    stock_data = stock_repo.get_stock_data("AAPL", "1mo")

    assert stock_data is None


# Test for creating stock in the database
def test_create_stock_db_interaction(mock_db_session):
    repo = StockRepositoryImpl(mock_db_session)  # Pass the mock session
    stock = Stock(
        "AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 150.0, "2023-09-01"
    )

    repo.create_stock(stock)

    mock_db_session.add.assert_called_once_with(stock)
    mock_db_session.commit.assert_called_once()


# Test for deleting stock when stock is not found in the database
def test_delete_stock_not_found_db(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
        None  # Stock not found
    )

    repo = StockRepositoryImpl(mock_db_session)  # Pass the mock session
    result = repo.delete_stock("AAPL")

    assert result is False
    mock_db_session.delete.assert_not_called()
