import pytest
from sqlalchemy import create_engine, MetaData
from unittest import mock
import importlib.util


# Dynamically import the migration script
def load_migration_module():
    module_name = "migration_14f96da0ec16_add_id_column_to_stocks_table"
    file_path = (
        "src/infrastructure/db/migrations/versions/"
        "14f96da0ec16_add_id_column_to_stocks_table.py"
    )
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    migration_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration_module)
    return migration_module


# Load the migration module
migration_module = load_migration_module()


@pytest.fixture(scope="function")
def connection():
    """Setup an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()

    # Begin a transaction explicitly for the test setup
    transaction = connection.begin()
    yield connection
    transaction.rollback()  # Rollback after each test
    connection.close()


def test_upgrade_adds_columns(connection):
    # Given: a connection to an empty in-memory SQLite database
    metadata = MetaData()
    metadata.reflect(bind=connection)  # Reflect existing tables

    # Mock the Alembic op object
    with mock.patch(
        "src.infrastructure.db.migrations.versions."
        "14f96da0ec16_add_id_column_to_stocks_table.op"
    ) as mocked_op:
        # Apply the upgrade migration
        migration_module.upgrade(mocked_op)

        # Verify the columns were added using the mocked op
        mocked_op.add_column.assert_any_call("stocks", mock.ANY)


def test_downgrade_removes_columns(connection):
    # Given: the "stocks" table exists with the new columns
    metadata = MetaData()
    metadata.reflect(bind=connection)  # Reflect existing tables

    # Mock the Alembic op object
    with mock.patch(
        "src.infrastructure.db.migrations.versions."
        "14f96da0ec16_add_id_column_to_stocks_table.op"
    ) as mocked_op:
        # Apply the upgrade migration
        migration_module.upgrade(mocked_op)

        # Apply the downgrade migration
        migration_module.downgrade(mocked_op)

        # Verify the columns were removed using the mocked op
        mocked_op.drop_column.assert_any_call("stocks", "market_cap")
