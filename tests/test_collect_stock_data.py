import pytest
from unittest.mock import MagicMock
from src.application.use_cases.collect_stock_data import CollectStockData
from src.domain.models.stock import Stock

# Test for a successful use case (valid data)
def test_collect_stock_data_success():
    # Simulate the repository returning valid data
    mock_repo = MagicMock()
    mock_repo.get_stock_data.return_value = {'close': 150, 'date': '2023-09-01'}
    
    use_case = CollectStockData(mock_repo)
    stock = use_case.execute('AAPL', '1mo')

    assert stock is not None
    assert stock.ticker == 'AAPL'
    assert stock.close_price == 150
    assert stock.date == '2023-09-01'

# Test when no data is found (None returned by the repository)
def test_collect_stock_data_no_data():
    # Simulate the repository returning None
    mock_repo = MagicMock()
    mock_repo.get_stock_data.return_value = None
    
    use_case = CollectStockData(mock_repo)
    stock = use_case.execute('AAPL', '1mo')

    assert stock is None

# Test when a connection error occurs (None returned by the repository)
def test_collect_stock_data_connection_error():
    # Simulate the repository returning None due to a connection error
    mock_repo = MagicMock()
    mock_repo.get_stock_data.return_value = None

    use_case = CollectStockData(mock_repo)
    stock = use_case.execute('AAPL', '1mo')

    assert stock is None
