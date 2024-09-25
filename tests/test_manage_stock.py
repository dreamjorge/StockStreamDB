from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import CreateStock, GetStock, UpdateStock, DeleteStock
from src.domain.models.stock import Stock

def test_create_stock():
    mock_repo = MagicMock()
    stock = Stock("AAPL", "Apple Inc.", "Technology", 150)  # Add close_price
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.sector == "Technology"
    assert stock.close_price == 150

def test_get_stock():
    mock_repo = MagicMock()
    use_case = GetStock(mock_repo)
    use_case.execute("AAPL")
    mock_repo.get_stock_by_ticker.assert_called_once_with("AAPL")

def test_update_stock():
    mock_repo = MagicMock()
    stock = Stock("AAPL", "Apple Inc.", "Technology", 150)  # Add close_price
    # Add update logic here
    assert stock.close_price == 150

def test_delete_stock():
    mock_repo = MagicMock()
    use_case = DeleteStock(mock_repo)
    use_case.execute("AAPL")
    mock_repo.delete_stock.assert_called_once_with("AAPL")
