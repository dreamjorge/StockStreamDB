from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import CreateStock, GetStock, UpdateStock, DeleteStock
from src.domain.models.stock import Stock

def test_create_stock():
    mock_repo = MagicMock()
    # Ensure the correct number of arguments
    stock = Stock("AAPL", "Apple Inc.", "Technology")  
    use_case = CreateStock(mock_repo)
    use_case.execute(stock)
    mock_repo.create_stock.assert_called_once_with(stock)

def test_get_stock():
    mock_repo = MagicMock()
    use_case = GetStock(mock_repo)
    use_case.execute("AAPL")
    mock_repo.get_stock_by_ticker.assert_called_once_with("AAPL")

def test_update_stock():
    mock_repo = MagicMock()
    # Ensure the correct number of arguments
    stock = Stock("AAPL", "Apple Inc.", "Technology")  
    use_case = UpdateStock(mock_repo)
    use_case.execute(stock)
    mock_repo.update_stock.assert_called_once_with(stock)

def test_delete_stock():
    mock_repo = MagicMock()
    use_case = DeleteStock(mock_repo)
    use_case.execute("AAPL")
    mock_repo.delete_stock.assert_called_once_with("AAPL")
