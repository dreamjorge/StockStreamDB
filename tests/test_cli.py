import pytest
import sys
from unittest.mock import patch, MagicMock
from src.interfaces.cli.cli import main
from src.application.use_cases.manage_stock import ManageStockUseCase

# Mocking StockRepositoryImpl and ManageStockUseCase.create_stock for the create action
@patch('src.infrastructure.db.stock_repository_impl.StockRepositoryImpl')
@patch('src.application.use_cases.manage_stock.ManageStockUseCase.create_stock')
def test_cli_create(mock_create_stock, mock_repository):
    sys.argv = ['cli.py', 'create', '--ticker', 'AAPL', '--name', 'Apple Inc.', '--industry', 'Technology', '--sector', 'Consumer Electronics', '--close_price', '150', '--date', '2023-09-01']
    
    main()

    # Ensure create_stock was called with the correct arguments
    mock_create_stock.assert_called_once_with(
        ticker='AAPL',
        name='Apple Inc.',
        industry='Technology',
        sector='Consumer Electronics',
        close_price=150,
        date='2023-09-01'
    )
    
    # Clear sys.argv after the test
    sys.argv = []

# Test missing required arguments, ensuring it raises SystemExit
@patch('src.infrastructure.db.stock_repository_impl.StockRepositoryImpl')
def test_cli_missing_arguments(mock_repository):
    sys.argv = ['cli.py', 'create', '--ticker', 'AAPL']  # Missing required arguments

    try:
        main()
        assert False, "Expected SystemExit but did not get it"
    except SystemExit:
        pass  # This is the expected behavior


# Mocking StockRepositoryImpl and ManageStockUseCase.update_stock for the update action
@patch('src.infrastructure.db.stock_repository_impl.StockRepositoryImpl')
@patch('src.application.use_cases.manage_stock.ManageStockUseCase.update_stock')
def test_cli_update(mock_update_stock, mock_repository):
    sys.argv = ['cli.py', 'update', '--ticker', 'AAPL', '--close_price', '160']
    
    main()

    # Ensure update_stock was called with the correct arguments
    mock_update_stock.assert_called_once_with(
        ticker='AAPL',
        name=None,
        industry=None,
        sector=None,
        close_price=160.0,
        date=None
    )
    
    # Clear sys.argv after the test
    sys.argv = []
