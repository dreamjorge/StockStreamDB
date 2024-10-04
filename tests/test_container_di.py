from src.application.use_cases.manage_stock import ManageStockUseCase
from src.containers import Container

def test_container_di():
    container = Container()
    stock_service = container.stock_service()  # Fetch the stock_service from container
    assert stock_service is not None  # Check if stock_service is correctly created
