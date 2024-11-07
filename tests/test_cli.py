# tests/test_cli.py

import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.interfaces.cli.cli import cli  # Import the click group
from datetime import datetime


class TestCLI(unittest.TestCase):
    @patch("src.interfaces.cli.cli.ManageStockUseCase")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_create(self, mock_get_session, mock_manage_stock_use_case_class):
        """Test the CLI create command."""
        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Create a mock instance of ManageStockUseCase
        mock_manage_stock_use_case_instance = (
            mock_manage_stock_use_case_class.return_value
        )

        # Set up the create_stock method to return a mock stock
        mock_manage_stock_use_case_instance.create_stock.return_value = MagicMock(
            ticker="AAPL"
        )

        # Define the command-line arguments
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "create",
                "AAPL",
                "Apple Inc.",
                "Technology",
                "Hardware",
                "150.00",
                "2023-01-01",
            ],
        )

        # Assert that the command exited without errors
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Created stock AAPL", result.output)

        # Assert that create_stock was called once with correct arguments
        mock_manage_stock_use_case_instance.create_stock.assert_called_once_with(
            ticker="AAPL",
            name="Apple Inc.",
            industry="Technology",
            sector="Hardware",
            close=150.00,
            date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        )

    @patch("src.interfaces.cli.cli.ManageStockUseCase")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_fetch(self, mock_get_session, mock_manage_stock_use_case_class):
        """Test the CLI fetch command."""
        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Create a mock instance of ManageStockUseCase
        mock_manage_stock_use_case_instance = (
            mock_manage_stock_use_case_class.return_value
        )

        # Ensure that check_stock_exists returns False, simulating no data in DB
        mock_manage_stock_use_case_instance.check_stock_exists.return_value = False

        # Mock the fetch_stock_data method to return a mock data object
        mock_fetch_data = [
            {
                "date": "2023-01-01",
                "close": 150,
                "open": 148,
                "high": 151,
                "low": 147,
                "volume": 100000,
            }
        ]
        mock_manage_stock_use_case_instance.fetch_stock_data.return_value = (
            mock_fetch_data
        )

        # Define the command-line arguments
        runner = CliRunner()
        result = runner.invoke(cli, ["fetch", "AAPL", "1mo"])

        # Assert that the command exited without errors
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Fetch complete for AAPL in the period 1mo.", result.output)

        # Assert that check_stock_exists was called once with correct arguments
        mock_manage_stock_use_case_instance.check_stock_exists.assert_called_once_with(
            "AAPL", "1mo"
        )

        # Assert that fetch_stock_data was called once with correct arguments
        mock_manage_stock_use_case_instance.fetch_stock_data.assert_called_once_with(
            "AAPL", "1mo"
        )

    @patch("src.interfaces.cli.cli.ManageStockUseCase")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_delete(self, mock_get_session, mock_manage_stock_use_case_class):
        """Test the CLI delete command."""
        # Simulate successful deletion
        mock_manage_stock_use_case_instance = (
            mock_manage_stock_use_case_class.return_value
        )
        mock_manage_stock_use_case_instance.delete_stock.return_value = True

        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        runner = CliRunner()
        result = runner.invoke(cli, ["delete", "AAPL"])

        # Assert that the command exited successfully (exit code 0)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Deleted stock AAPL", result.output)

        # Assert that delete_stock was called once with correct arguments
        mock_manage_stock_use_case_instance.delete_stock.assert_called_once_with("AAPL")

    @patch("src.interfaces.cli.cli.ManageStockUseCase")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_delete_stock_not_found(
        self, mock_get_session, mock_manage_stock_use_case_class
    ):
        """Test delete command when the stock is not found."""
        # Simulate stock not found (delete_stock returns False)
        mock_manage_stock_use_case_instance = (
            mock_manage_stock_use_case_class.return_value
        )
        mock_manage_stock_use_case_instance.delete_stock.return_value = False

        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        runner = CliRunner()
        result = runner.invoke(cli, ["delete", "AAPL"])

        # Assert that the command exited with an error (exit code 1 due to
        # ClickException)
        self.assertEqual(result.exit_code, 1)

        # Assert that the error message is correct
        self.assertIn("Error: Stock with ticker AAPL not found.", result.output)

    @patch("src.interfaces.cli.cli.ManageStockUseCase")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_create_with_invalid_date(
        self, mock_get_session, mock_manage_stock_use_case_class
    ):
        """Test the CLI create command with invalid date."""
        # Set up the mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Create a mock instance of ManageStockUseCase
        mock_manage_stock_use_case_instance = (
            mock_manage_stock_use_case_class.return_value
        )

        runner = CliRunner()

        result = runner.invoke(
            cli,
            [
                "create",
                "AAPL",
                "Apple Inc.",
                "Technology",
                "Consumer Electronics",
                "150",
                "invalid-date",  # Invalid date format
            ],
        )

        # Assert that the command exited with an error
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: Invalid value for 'DATE'", result.output)

        # Ensure that create_stock was not called
        mock_manage_stock_use_case_instance.create_stock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
