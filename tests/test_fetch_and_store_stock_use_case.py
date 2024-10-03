from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher

@patch('yfinance.Ticker')
def test_fetch_stock_data(mock_ticker):
    # Create a mock for the history method
    mock_history = MagicMock()
    mock_history.return_value = pd.DataFrame({
        'Open': [228.46],
        'High': [229.52],
        'Low': [227.30],
        'Close': [227.79],
        'Volume': [33993600],
    }, index=pd.to_datetime(['2024-09-27']))

    # Assign the mock history method to the mock Ticker object
    mock_ticker.return_value.history = mock_history

    # Create an instance of the fetcher and fetch data
    fetcher = YahooFinanceFetcher()
    result = fetcher.fetch('AAPL', '1mo')

    # Check if result is not None
    assert result is not None, "The fetcher returned None, expected valid data."

    # Since result is a list, access the first element
    first_record = result[0]

    # Assert that the returned data contains the correct values in a dictionary format
    assert first_record['close'] == pytest.approx(227.79, rel=1e-5)
    assert first_record['date'] == '2024-09-27'
    assert first_record['open'] == pytest.approx(228.46, rel=1e-5)
    assert first_record['high'] == pytest.approx(229.52, rel=1e-5)
    assert first_record['low'] == pytest.approx(227.30, rel=1e-5)
    assert first_record['volume'] == 33993600
