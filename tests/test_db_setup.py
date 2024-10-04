import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from src.infrastructure.db.db_setup import init_db, get_session, Base, engine

# Test for init_db function
def test_init_db(mocker):
    # Mock the Base.metadata.create_all method to avoid creating actual tables
    mock_create_all = mocker.patch.object(Base.metadata, 'create_all', autospec=True)

    # Call the init_db function
    init_db()

    # Assert that the create_all method was called with the correct engine
    mock_create_all.assert_called_once_with(engine)


# Test for get_session context manager (successful transaction)
def test_get_session_success(mocker):
    # Mock the session
    mock_session = MagicMock(spec=Session)

    # Patch the sessionmaker to return the mock session
    mocker.patch('src.infrastructure.db.db_setup.SessionLocal', return_value=mock_session)

    # Use the context manager to get the session and simulate a successful transaction
    with get_session() as session:
        assert session == mock_session
        mock_session.commit.assert_not_called()

    # Ensure that commit is called once and session is closed
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


# Test for get_session context manager (failed transaction)
def test_get_session_failure(mocker):
    # Mock the session
    mock_session = MagicMock(spec=Session)

    # Patch the sessionmaker to return the mock session
    mocker.patch('src.infrastructure.db.db_setup.SessionLocal', return_value=mock_session)

    # Simulate an exception during the transaction
    with pytest.raises(Exception):
        with get_session() as session:
            assert session == mock_session
            raise Exception("Test exception")

    # Ensure that rollback is called and session is closed
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
