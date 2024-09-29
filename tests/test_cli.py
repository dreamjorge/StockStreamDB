# tests/test_cli.py

import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.interfaces.cli.cli import cli  # Import the click group

class TestCLI:
    @patch('src.interfaces.cli.cli.get_session')  # Mock get_session in cli.py
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.create_stock')  # Mock create_stock
    def test_cli_create(self, mock_create_stock, mock_get_session):
        """Test the CLI create command."""
        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Initialize CliRunner
        runner = CliRunner()

        # Define the command-line arguments
        result = runner.invoke(cli, [
            'create',
            'AAPL',
            'Apple Inc.',
            'Technology',
            'Consumer Electronics',
            '150',
            '2023-09-01'
        ])

        # Assert that the command exited without errors
        assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}"

        # Assert that create_stock was called once
        mock_create_stock.assert_called_once()

        # Optionally, check the output
        assert "Created stock AAPL" in result.output

    @patch('src.interfaces.cli.cli.get_session')  # Mock get_session in cli.py
    @patch('src.application.use_cases.manage_stock.ManageStockUseCase.fetch_stock_data')  # Mock fetch_stock_data
    def test_cli_fetch(self, mock_fetch_stock_data, mock_get_session):
        """Test the CLI fetch command."""
        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

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

        # Optionally, check the output
        assert "Sample Data" in result.output
