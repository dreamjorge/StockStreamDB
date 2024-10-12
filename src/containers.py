from dependency_injector import containers, providers
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from src.use_cases.stock_service import StockService  # Import your StockService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Container(containers.DeclarativeContainer):
    # Database configuration
    engine = create_engine("sqlite:///src/infrastructure/db/database.db")
    session = providers.Singleton(sessionmaker(bind=engine))

    # Repositories
    stock_repository = providers.Factory(StockRepositoryImpl, session=session)

    # Fetchers
    stock_fetcher = providers.Factory(YahooFinanceFetcher)

    # Services
    stock_service = providers.Factory(
        StockService, stock_repository=stock_repository, stock_fetcher=stock_fetcher
    )
