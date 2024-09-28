import pytest
import sys
from unittest.mock import patch, MagicMock
from src.interfaces.cli.cli import main
from src.domain.models.stock import Stock

@pytest.fixture
def mock_stock_repository():
    """Fixture to mock StockRepositoryImpl."""
    with patch('src.infrastructure.db.stock_repository_impl.StockRepositoryImpl') as mock_repo:
        yield mock_repo

@pytest.fixture
def mock_manage_stock_use_case():
    """Fixture to mock ManageStockUseCase."""
    with patch('src.application.use_cases.manage_stock.ManageStockUseCase') as mock_use_case:
        yield mock_use_case

class TestCLI:
    
    def teardown_method(self):
        """Reset sys.argv after every test."""
        sys.argv = []

    def assert_stock_object(self, stock_passed, expected):
        """Helper function to assert stock object fields."""
        assert stock_passed.ticker == expected['ticker']
        assert stock_passed.name == expected['name']
        assert stock_passed.industry == expected['industry']
        assert stock_passed.sector == expected['sector']
        assert stock_passed.close_price == expected['close_price']
        assert str(stock_passed.date) == expected['date']

    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.create_stock')
    def test_cli_create(self, mock_create_stock, mock_stock_repository):
        """Test the CLI create command."""
        sys.argv = ['cli.py', 'create', 'AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics', '150', '2023-09-01']
        
        main()

        mock_create_stock.assert_called_once()

        stock_passed = mock_create_stock.call_args[0][0]
        
        expected_stock = {
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'industry': 'Technology',
            'sector': 'Consumer Electronics',
            'close_price': 150.0,
            'date': '2023-09-01'
        }
        self.assert_stock_object(stock_passed, expected_stock)

    def test_cli_missing_arguments(self, mock_stock_repository):
        """Test missing arguments for create command."""
        sys.argv = ['cli.py', 'create', '--ticker', 'AAPL']

        with pytest.raises(SystemExit):
            main()

    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.update_stock')
    def test_cli_update(self, mock_update_stock, mock_stock_repository):
        """Test the CLI update command."""
        sys.argv = ['cli.py', 'update', 'AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics', '160', '2023-09-02']
        
        main()

        mock_update_stock.assert_called_once()

        stock_passed = mock_update_stock.call_args[0][0]

        expected_stock = {
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'industry': 'Technology',
            'sector': 'Consumer Electronics',
            'close_price': 160.0,
            'date': '2023-09-02'
        }
        self.assert_stock_object(stock_passed, expected_stock)

    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.get_stock')
    def test_cli_get(self, mock_get_stock, mock_stock_repository):
        """Test the CLI get command."""
        sys.argv = ['cli.py', 'get', 'AAPL']
        
        # Mock the return value
        mock_get_stock.return_value = Stock(ticker='AAPL', name='Apple Inc.', industry='Technology', sector='Consumer Electronics', close_price=150.0, date='2023-09-01')

        main()

        # Ensure get_stock was called with 'AAPL'
        mock_get_stock.assert_called_once_with('AAPL')

    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.delete_stock')
    def test_cli_delete(self, mock_delete_stock, mock_stock_repository):
        """Test the CLI delete command."""
        sys.argv = ['cli.py', 'delete', 'AAPL']
        
        main()

        # Ensure delete_stock was called with 'AAPL'
        mock_delete_stock.assert_called_once_with('AAPL')

    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.delete_stock')
    def test_cli_delete_not_found(self, mock_delete_stock, mock_stock_repository):
        """Test the CLI delete command when stock is not found."""
        sys.argv = ['cli.py', 'delete', 'AAPL']
        
        # Simulate stock not found (delete_stock returns False)
        mock_delete_stock.return_value = False
        
        main()

        mock_delete_stock.assert_called_once_with('AAPL')