from unittest.mock import MagicMock
import pytest
from datetime import datetime
from src.application.use_cases.collect_stock_data import CollectStockData
from math import isclose


@pytest.fixture
def mock_stock_fetcher_service():
    return MagicMock()


@pytest.fixture
def use_case(mock_stock_fetcher_service):
    return CollectStockData(stock_fetcher_service=mock_stock_fetcher_service)


def test_collect_stock_data_success(use_case, mock_stock_fetcher_service):
    # Mock fetch return value
    mock_stock_fetcher_service.fetch.return_value = {
        'ticker': 'AAPL',
        'name': 'Apple Inc.',
        'industry': 'Technology',
        'sector': 'Consumer Electronics',
        'close': 227.34,
        'date': datetime(2024, 9, 26)
    }

    # Execute the use case
    stock = use_case.execute('AAPL')

    # Assert that fetch was called with the correct arguments
    mock_stock_fetcher_service.fetch.assert_called_once_with('AAPL')

    # Assert that the returned stock has the expected values
    assert stock['ticker'] == 'AAPL'
    assert stock['name'] == 'Apple Inc.'
    assert isclose(stock['close'], 227.34, rel_tol=1e-9)
    assert stock['date'] == datetime(2024, 9, 26)


def test_collect_stock_data_invalid_period(use_case):
    # Test with an invalid period
    with pytest.raises(ValueError, match="Invalid period"):
        use_case.execute('AAPL', '10y')


def test_collect_stock_data_no_data(use_case, mock_stock_fetcher_service):
    # Mock fetch to return None
    mock_stock_fetcher_service.fetch.return_value = None

    # Execute the use case
    result = use_case.execute('AAPL')

    # Assert that fetch was called
    mock_stock_fetcher_service.fetch.assert_called_once_with('AAPL')

    # Assert that no stock is returned when data is None
    assert result is None


def test_collect_stock_data_prints_no_data_message(capfd, use_case, mock_stock_fetcher_service):
    # Mock fetch to return None
    mock_stock_fetcher_service.fetch.return_value = None

    # Execute the use case
    result = use_case.execute('AAPL')

    # Capture stdout and check for the correct message
    captured = capfd.readouterr()
    assert "No data found for AAPL." in captured.out

    # Assert that no stock is returned
    assert result is None


def test_collect_stock_data_with_various_periods(use_case, mock_stock_fetcher_service):
    # Mock fetch return value
    mock_stock_fetcher_service.fetch.return_value = {
        'ticker': 'AAPL',
        'name': 'Apple Inc.',
        'industry': 'Technology',
        'sector': 'Consumer Electronics',
        'close': 227.34,
        'date': datetime(2024, 9, 26)
    }

    # Test with multiple valid periods
    for period in ['1mo', '3mo', '6mo', '1y', '5y']:
        stock = use_case.execute('AAPL')

        # Assert that fetch was called with the correct arguments
        mock_stock_fetcher_service.fetch.assert_called_with('AAPL')

        # Assert that the returned stock has the expected values
        assert stock['ticker'] == 'AAPL'
        assert stock['name'] == 'Apple Inc.'
        assert isclose(stock['close'], 227.34, rel_tol=1e-9)
        assert stock['date'] == datetime(2024, 9, 26)
