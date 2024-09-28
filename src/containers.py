from dependency_injector import containers, providers
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl

class Container(containers.DeclarativeContainer):
    stock_repository = providers.Factory(StockRepositoryImpl)
    stock_service = providers.Factory(ManageStockUseCase, stock_repository=stock_repository)
