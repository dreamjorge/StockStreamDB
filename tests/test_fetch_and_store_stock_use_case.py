import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from src.application.use_cases.fetch_and_store_stock_use_case import FetchAndStoreStockUseCase
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher

@pytest.fixture
def yahoo_finance_fetcher():
    # Mock YahooFinanceFetcher to return a dictionary
    mock_fetcher = MagicMock()

    # Create a mock dictionary to represent stock data
    mock_data = {
        'ticker': 'AAPL',
        'close_price': 150.0,
        'date': '2023-09-01',
        'open': 145.0,
        'high': 146.0,
        'low': 144.0,
        'volume': 1000000
    }

    # Configure the fetcher to return the mock dictionary
    mock_fetcher.fetch.return_value = mock_data
    return mock_fetcher

@pytest.fixture
def stock_repository():
    # Mock StockRepositoryImpl
    mock_repo = MagicMock()
    return mock_repo

def test_fetch_and_store_stock(yahoo_finance_fetcher, stock_repository):
    # Create the use case with the mocked fetcher and repository
    use_case = FetchAndStoreStockUseCase(yahoo_finance_fetcher, stock_repository)

    # Execute the use case
    use_case.execute("AAPL", "1mo")

    # Verify that the fetcher was called with the correct arguments
    yahoo_finance_fetcher.fetch.assert_called_once_with("AAPL", "1mo")

    # Verify that stock data was saved using the repository
    stock_repository.create_stock.assert_called_once()  # Only one recent row is saved

@patch('yfinance.download')
def test_fetch_stock_data(mock_download):
    # Mock the return value of yfinance.download to simulate fetched stock data
    mock_download.return_value = pd.DataFrame({
        'Open': [228.46],
        'High': [229.52],
        'Low': [227.30],
        'Close': [227.79],
        'Volume': [33993600],  # Update the volume to match the actual value
    }, index=pd.to_datetime(['2024-09-27']))
    
    fetcher = YahooFinanceFetcher()
    result = fetcher.fetch('AAPL', '1mo')
    
    # Assert that the returned data contains the correct values in a dictionary format
    assert result['close_price'] == pytest.approx(227.79, rel=1e-5)
    assert result['ticker'] == 'AAPL'
    assert result['date'] == '2024-09-27'
    assert result['open'] == pytest.approx(228.46, rel=1e-5)
    assert result['high'] == pytest.approx(229.52, rel=1e-5)
    assert result['low'] == pytest.approx(227.30, rel=1e-5)
    assert result['volume'] == 33993600  # Update expected volume



