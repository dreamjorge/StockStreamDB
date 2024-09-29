import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.application.use_cases.fetch_and_store_stock_use_case import FetchAndStoreStockUseCase
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from unittest.mock import patch

@pytest.fixture
def yahoo_finance_fetcher():
    # Mock YahooFinanceFetcher to return a DataFrame
    mock_fetcher = MagicMock()
    
    # Create a mock DataFrame similar to the data you'd get from yfinance
    data = {
        "Open": [145.0, 146.0],
        "High": [146.0, 147.0],
        "Low": [144.0, 145.0],
        "Close": [145.5, 146.5],
        "Volume": [1000000, 2000000]
    }
    mock_df = pd.DataFrame(data, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
    
    # Configure the fetcher to return the mock DataFrame
    mock_fetcher.fetch.return_value = mock_df
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
    assert stock_repository.save.call_count == 2  # Two rows of stock data

@patch('yfinance.download')
def test_fetch_stock_data(mock_download):
    mock_download.return_value = pd.DataFrame({'Close': [150.0], 'Date': ['2023-09-01']})
    
    fetcher = YahooFinanceFetcher()
    result = fetcher.fetch('AAPL', '1mo')

    assert result['Close'].iloc[0] == pytest.approx(226.49, rel=1e-5)
