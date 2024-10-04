# tests/test_cli.py

import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.interfaces.cli.cli import cli  # Import the click group


class TestCLI:
    @patch('src.interfaces.cli.cli.get_session')
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.create_stock')
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.__init__', return_value=None)
    def test_cli_create(self, mock_init, mock_create_stock, mock_get_session):
        """Test the CLI create command."""
        # Set up the mock session and stock_fetcher
        mock_session = MagicMock()
        mock_stock_fetcher = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_init.return_value = None  # To prevent instantiation errors

        # Define the command-line arguments
        runner = CliRunner()
        result = runner.invoke(cli, [
            'create',
            'AAPL',
            'Apple Inc.',
            'Technology',
            'Hardware',
            '150.00',
            '2023-01-01'
        ])

        # Assert that the command exited without errors
        assert result.exit_code == 0


    @patch('src.interfaces.cli.cli.get_session')  # Mock get_session in cli.py
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.fetch_stock_data')  # Mock fetch_stock_data
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.check_stock_exists')  # Mock check_stock_exists
    def test_cli_fetch(self, mock_check_stock_exists, mock_fetch_stock_data, mock_get_session):
        """Test the CLI fetch command."""
        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Ensure that check_stock_exists returns False, simulating no data in DB
        mock_check_stock_exists.return_value = False

        # Mock the fetch_stock_data method to return a mock data object
        mock_data = MagicMock()
        mock_data.empty = False
        mock_data.to_string.return_value = "Sample Data"
        mock_fetch_stock_data.return_value = mock_data

        # Initialize CliRunner
        runner = CliRunner()

        # Define the command-line arguments
        result = runner.invoke(cli, [
            'fetch',
            'AAPL',
            '1mo'
        ])

        # Assert that the command exited without errors
        assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}"

        # Assert that fetch_stock_data was called once with correct arguments
        mock_fetch_stock_data.assert_called_once_with('AAPL', '1mo')


    @patch('src.interfaces.cli.cli.get_session')  # Mock get_session in cli.py
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.create_stock')
    def test_cli_create_with_invalid_date(self, mock_create_stock, mock_get_session):
        """Test the CLI create command with invalid date."""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        runner = CliRunner()

        result = runner.invoke(cli, [
            'create',
            'AAPL',
            'Apple Inc.',
            'Technology',
            'Consumer Electronics',
            '150',
            'invalid-date'  # Invalid date format
        ])

        # Assert that the command exited with an error
        assert result.exit_code != 0
        assert "Error: Invalid value for 'DATE'" in result.output
        mock_create_stock.assert_not_called()  # Ensure that stock creation was not called

    @patch('src.interfaces.cli.cli.get_session')
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.delete_stock')
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.__init__', return_value=None)
    def test_cli_delete(self, mock_init, mock_delete_stock, mock_get_session):
        """Test the CLI delete command."""
        # Simulate successful deletion
        mock_delete_stock.return_value = True
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_init.return_value = None  # To prevent instantiation errors

        runner = CliRunner()
        result = runner.invoke(cli, ['delete', 'AAPL'])

        # Assert that the command exited successfully (exit code 0)
        assert result.exit_code == 0

    @patch('src.interfaces.cli.cli.get_session')
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.delete_stock')
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.__init__', return_value=None)
    def test_cli_delete_stock_not_found(self, mock_init, mock_delete_stock, mock_get_session):
        """Test delete command when the stock is not found."""
        # Simulate stock not found (delete_stock returns False)
        mock_delete_stock.return_value = False
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_init.return_value = None  # To prevent instantiation errors

        runner = CliRunner()
        result = runner.invoke(cli, ['delete', 'AAPL'])

        # Assert that the command exited with an error (exit code 1 due to ClickException)
        assert result.exit_code == 1

        # Assert that the error message is correct
        assert "Error: Stock with ticker AAPL not found." in result.output