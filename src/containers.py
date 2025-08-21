from dependency_injector import containers, providers
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.infrastructure.fetchers.stock_fetcher import StockFetcher
from src.use_cases.stock_service import StockService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Container(containers.DeclarativeContainer):
    """Dependency injection container for the application."""

    # Database configuration
    engine = create_engine("sqlite:///src/infrastructure/db/database.db")
    """The database engine."""

    session = providers.Singleton(sessionmaker(bind=engine))
    """The database session."""

    # Repositories
    stock_repository = providers.Factory(StockRepositoryImpl, session=session)
    """The stock repository."""

    # Fetchers
    stock_fetcher = providers.Factory(StockFetcher)
    """The stock fetcher."""

    # Services
    stock_service = providers.Factory(
        StockService, stock_repository=stock_repository, stock_fetcher=stock_fetcher
    )
    """The stock service."""
