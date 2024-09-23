import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.infrastructure.db.stock_repository import StockRepository
from requests.exceptions import RequestException

# Test for a successful connection and valid data
@patch('yfinance.Ticker')
def test_get_stock_data_success(mock_ticker):
    # Simulate a valid pandas DataFrame
    mock_history = MagicMock()
    mock_df = pd.DataFrame({
        'Close': [150],
    }, index=['2023-09-01'])  # Create a valid DataFrame with a 'Close' column
    
    mock_history.history.return_value = mock_df
    mock_ticker.return_value = mock_history

    stock_repo = StockRepository()
    stock_data = stock_repo.get_stock_data('AAPL', '1mo')

    assert stock_data is not None
    assert stock_data['close'] == 150
    assert stock_data['date'] == '2023-09-01'

# Test when no data is found (empty DataFrame)
@patch('yfinance.Ticker')
def test_get_stock_data_no_data(mock_ticker):
    # Simulate an empty DataFrame
    mock_history = MagicMock()
    mock_df = pd.DataFrame()  # Empty DataFrame
    mock_history.history.return_value = mock_df
    mock_ticker.return_value = mock_history

    stock_repo = StockRepository()
    stock_data = stock_repo.get_stock_data('AAPL', '1mo')

    assert stock_data is None

# Test to simulate a connection error (RequestException)
@patch('yfinance.Ticker')
def test_get_stock_data_connection_error(mock_ticker):
    # Simulate a connection exception
    mock_history = MagicMock()
    mock_history.history.side_effect = RequestException("Connection error")
    mock_ticker.return_value = mock_history

    stock_repo = StockRepository()
    stock_data = stock_repo.get_stock_data('AAPL', '1mo')

    assert stock_data is None
