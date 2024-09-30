# src/containers.py

from src.infrastructure.db.db_setup import get_session
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.application.use_cases.manage_stock import ManageStockUseCase
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    session = providers.Factory(get_session)
    
    stock_repository = providers.Factory(
        StockRepositoryImpl,
        session=session
    )
    
    stock_service = providers.Factory(
        ManageStockUseCase,
        stock_repository=stock_repository
    )
