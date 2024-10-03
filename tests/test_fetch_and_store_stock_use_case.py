import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
import pandas as pd

@pytest.fixture
def fetcher():
    return YahooFinanceFetcher()

@patch('yfinance.Ticker')
def test_fetch_list_format(mock_ticker, fetcher):
    # Mock stock data returned by yfinance
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame({
        'Open': [150.0],
        'High': [155.0],
        'Low': [149.0],
        'Close': [152.0],
        'Volume': [1000000],
    }, index=pd.to_datetime(['2023-09-01']))
    
    mock_ticker.return_value.history = mock_history
    
    result = fetcher.fetch('AAPL', return_format='list')
    
    # Verify result format and values
    assert isinstance(result, list)
    assert result == [{
        'ticker': 'AAPL',
        'date': '2023-09-01',
        'close': 152.0,
        'open': 150.0,
        'high': 155.0,
        'low': 149.0,
        'volume': 1000000
    }]

@patch('yfinance.Ticker')
def test_fetch_dict_format(mock_ticker, fetcher):
    # Mock stock data returned by yfinance
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame({
        'Open': [150.0],
        'High': [155.0],
        'Low': [149.0],
        'Close': [152.0],
        'Volume': [1000000],
    }, index=pd.to_datetime(['2023-09-01']))
    
    mock_ticker.return_value.history = mock_history
    
    result = fetcher.fetch('AAPL', return_format='dict')
    
    # Verify result format and values
    assert isinstance(result, dict)
    assert result == {
        '2023-09-01': {
            'ticker': 'AAPL',
            'close': 152.0,
            'open': 150.0,
            'high': 155.0,
            'low': 149.0,
            'volume': 1000000
        }
    }

@patch('yfinance.Ticker')
def test_fetch_dataframe_format(mock_ticker, fetcher):
    # Mock stock data returned by yfinance
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame({
        'Open': [150.0],
        'High': [155.0],
        'Low': [149.0],
        'Close': [152.0],
        'Volume': [1000000],
    }, index=pd.to_datetime(['2023-09-01']))
    
    mock_ticker.return_value.history = mock_history
    
    result = fetcher.fetch('AAPL', return_format='dataframe')
    
    # Verify result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 5)  # 1 row, 5 columns
    assert list(result.columns) == ['Open', 'High', 'Low', 'Close', 'Volume']

@patch('yfinance.Ticker')
def test_fetch_no_data(mock_ticker, fetcher):
    # Mock an empty DataFrame returned by yfinance
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame()
    
    mock_ticker.return_value.history = mock_history
    
    result = fetcher.fetch('AAPL', return_format='list')
    
    # Verify empty result
    assert result == []

@patch('yfinance.Ticker')
def test_fetch_invalid_format(mock_ticker, fetcher):
    # Mock stock data returned by yfinance
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame({
        'Open': [150.0],
        'High': [155.0],
        'Low': [149.0],
        'Close': [152.0],
        'Volume': [1000000],
    }, index=pd.to_datetime(['2023-09-01']))
    
    mock_ticker.return_value.history = mock_history
    
    # Test unsupported return format
    with pytest.raises(ValueError, match="Unsupported return_format"):
        fetcher.fetch('AAPL', return_format='unsupported_format')

@patch('yfinance.Ticker')
def test_fetch_exception_handling(mock_ticker, fetcher):
    # Simulate an exception thrown by yfinance
    mock_ticker.return_value.history.side_effect = Exception("Network Error")
    
    result = fetcher.fetch('AAPL')
    
    # Verify that the fetch method handles the exception and returns None
    assert result is None

@patch('yfinance.Ticker')
def test_fetch_partial_data(mock_ticker, fetcher):
    # Mock stock data with missing fields (e.g., missing 'Volume')
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame({
        'Open': [150.0],
        'High': [155.0],
        'Low': [149.0],
        'Close': [152.0],
    }, index=pd.to_datetime(['2023-09-01']))
    
    mock_ticker.return_value.history = mock_history
    
    result = fetcher.fetch('AAPL', return_format='list')
    
    # Verify result handles missing fields gracefully
    assert result == [{
        'ticker': 'AAPL',
        'date': '2023-09-01',
        'close': 152.0,
        'open': 150.0,
        'high': 155.0,
        'low': 149.0,
        'volume': None  # 'Volume' was missing
    }]
