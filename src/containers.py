# In your container configuration (src/containers.py)

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
    
    # Provide a simple mock stock_fetcher or a real implementation
    stock_fetcher = providers.Object(lambda ticker, period: [])

    stock_service = providers.Factory(
        ManageStockUseCase,
        stock_repo=stock_repository,
        stock_fetcher=stock_fetcher  # Pass the mock or actual fetcher
    )
