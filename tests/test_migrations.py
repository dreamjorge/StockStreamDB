from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
import pytest

# Assuming Base is the declarative_base from your models.py
from src.infrastructure.db.models import Base


@pytest.fixture(scope="function")
def setup_database():
    # Create an in-memory SQLite database or test database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)  # Create tables in the test database

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


def test_migration_setup(setup_database):
    # Point to the Alembic configuration
    alembic_cfg = Config("config/alembic.ini")

    # Run Alembic upgrade to the latest migration
    command.upgrade(alembic_cfg, "head")

    # Verify the tables were created properly
    session = setup_database
    result = session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table';")
    ).fetchall()

    expected_tables = ["stocks", "stock_prices", "fundamentals", "sentiment_analysis"]
    table_names = [row[0] for row in result]

    for table in expected_tables:
        assert table in table_names


def test_insert_data_after_migration(setup_database):
    session = setup_database

    # Insert some stock data into the migrated schema
    session.execute(
        text(
            "INSERT INTO stocks (ticker, name, industry, sector) "
            "VALUES ('AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics')"
        )
    )
    session.commit()

    # Fetch the inserted data and verify it
    result = session.execute(
        text("SELECT * FROM stocks WHERE ticker = 'AAPL';")
    ).fetchone()

    assert result is not None
    assert result[1] == "Apple Inc."  # Use tuple indexing to access the result fields
    assert result[2] == "Technology"
    assert result[3] == "Consumer Electronics"


# TODO: It needed verify downgrade migration
# def test_downgrade_migration(setup_database):
#     alembic_cfg = Config("alembic.ini")

#     # Upgrade to the latest migration
#     command.upgrade(alembic_cfg, "head")

#     # Downgrade to a previous migration
#     command.downgrade(alembic_cfg, "-1")

#     session = setup_database

#     # Verify the tables after the downgrade
#     result = session.execute(text("SELECT name
#     FROM sqlite_master WHERE type='table';")).fetchall()
#     downgraded_tables = [row[0] for row in result]

#     # Check that the 'sentiment_analysis' table is not present after downgrade
#     assert 'sentiment_analysis' not in downgraded_tables
