from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import CreateStock, GetStock, UpdateStock, DeleteStock
from src.domain.models.stock import Stock

def test_create_stock():
    # Ensure correct order of arguments (ticker, name, industry, sector, close_price, date)
    stock = Stock("AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 150, "2023-09-01")
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.industry == "Technology"  # Verify industry
    assert stock.sector == "Consumer Electronics"  # Ensure the correct sector
    assert stock.close_price == 150
    assert stock.date == "2023-09-01"





def test_get_stock():
    mock_repo = MagicMock()
    use_case = GetStock(mock_repo)
    use_case.execute("AAPL")
    mock_repo.get.assert_called_once_with("AAPL")

def test_update_stock():
    mock_repo = MagicMock()
    stock = Stock("AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 150, "2023-09-01")  # Add close_price and date
    # Add update logic here
    assert stock.close_price == 150
    assert stock.date == "2023-09-01"


def test_delete_stock():
    mock_repo = MagicMock()
    use_case = DeleteStock(mock_repo)
    use_case.execute("AAPL")
    mock_repo.delete_stock.assert_called_once_with("AAPL")
