from unittest.mock import MagicMock
import pytest
from datetime import datetime
from src.application.use_cases.collect_stock_data import CollectStockData
from math import isclose

def test_collect_stock_data():
    # Mock the stock fetcher
    mock_fetcher = MagicMock()
    
    # Mock fetch return value
    mock_fetcher.fetch.return_value = {
        'ticker': 'AAPL',
        'name': 'Apple Inc.',
        'industry': 'Technology',
        'sector': 'Consumer Electronics',
        'close': 227.34,
        'date': datetime(2024, 9, 26)
    }

    # Create instance of CollectStockData with the mocked fetcher
    use_case = CollectStockData(mock_fetcher)
    
    # Execute the use case
    stock = use_case.execute('AAPL', '1mo')
    
    # Assert that fetch was called with the correct arguments
    mock_fetcher.fetch.assert_called_once_with('AAPL', '1mo')
    
    # Assert that the returned stock has the expected values
    assert stock.ticker == 'AAPL'
    assert stock.name == 'Apple Inc.'
    assert isclose(stock.close_price, 227.34, rel_tol=1e-9)
    assert stock.date == datetime(2024, 9, 26)
