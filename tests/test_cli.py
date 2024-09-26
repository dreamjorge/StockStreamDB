import sys
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

@patch('src.interfaces.cli.cli.YahooFinanceFetcher')
def test_cli_fetch(mock_fetcher):
    # Simulate CLI arguments
    test_args = ["cli.py", "fetch", "AAPL", "1mo"]
    with patch.object(sys, 'argv', test_args):
        # Mock the fetch method of the fetcher
        mock_fetcher_instance = mock_fetcher.return_value
        mock_fetcher_instance.fetch.return_value = {
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'industry': 'Technology',
            'sector': 'Consumer Electronics',
            'close': 227.34,
            'date': datetime(2024, 9, 26)
        }

        # Import the CLI main function and run it
        from src.interfaces.cli.cli import main
        main()

        # Assertions to ensure the mock fetch is called with the correct arguments
        mock_fetcher_instance.fetch.assert_called_once_with('AAPL', '1mo')


@patch('src.interfaces.cli.cli.YahooFinanceFetcher')
def test_cli_fetch_invalid_period(mock_fetcher):
    # Simulate CLI arguments with an invalid period
    test_args = ["cli.py", "fetch", "AAPL", "invalid_period"]
    with patch.object(sys, 'argv', test_args):
        # Mock the fetch method to raise an exception for invalid period
        mock_fetcher_instance = mock_fetcher.return_value
        mock_fetcher_instance.fetch.side_effect = ValueError("Invalid period")
        
        # Import the CLI main function and expect ValueError
        from src.interfaces.cli.cli import main
        with pytest.raises(ValueError, match="Invalid period"):
            main()


@patch('src.interfaces.cli.cli.CreateStock')
@patch('src.interfaces.cli.cli.StockRepositoryImpl')
def test_cli_create(mock_stock_repo, mock_create_stock):
    # Simulate CLI arguments for the create command
    test_args = ["cli.py", "create", "AAPL", "Apple Inc.", "Technology", "Consumer Electronics", "227.34", "2024-09-26"]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main

        # Mock repository and use case behavior
        mock_repo_instance = mock_stock_repo.return_value
        mock_create_stock_instance = mock_create_stock.return_value

        main()

        # Verify that the CreateStock use case was called
        mock_create_stock_instance.execute.assert_called_once()
        print(f"Created stock with ticker {mock_create_stock_instance.execute.call_args[0][0].ticker}")


@patch('src.interfaces.cli.cli.UpdateStock')
@patch('src.interfaces.cli.cli.StockRepositoryImpl')
def test_cli_update(mock_stock_repo, mock_update_stock):
    # Simulate CLI arguments for the update command
    test_args = ["cli.py", "update", "AAPL", "Apple Corporation", "Technology", "Consumer Electronics", "230.00", "2024-10-01"]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main

        # Mock repository and use case behavior
        mock_repo_instance = mock_stock_repo.return_value
        mock_update_stock_instance = mock_update_stock.return_value

        main()

        # Verify that the UpdateStock use case was called
        mock_update_stock_instance.execute.assert_called_once()
        print(f"Updated stock with ticker {mock_update_stock_instance.execute.call_args[0][0].ticker}")


@patch('src.interfaces.cli.cli.DeleteStock')
@patch('src.interfaces.cli.cli.StockRepositoryImpl')
def test_cli_delete(mock_stock_repo, mock_delete_stock):
    # Simulate CLI arguments for the delete command
    test_args = ["cli.py", "delete", "AAPL"]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main

        # Mock repository and use case behavior
        mock_repo_instance = mock_stock_repo.return_value
        mock_delete_stock_instance = mock_delete_stock.return_value

        main()

        # Verify that the DeleteStock use case was called
        mock_delete_stock_instance.execute.assert_called_once_with("AAPL")
        print(f"Deleted stock with ticker {mock_delete_stock_instance.execute.call_args[0][0]}")
