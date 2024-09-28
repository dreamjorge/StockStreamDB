from src.application.use_cases.manage_stock import ManageStockUseCase
from src.containers import Container

def test_container_di():
    container = Container()
    stock_service = container.stock_service()

    assert isinstance(stock_service, ManageStockUseCase)
