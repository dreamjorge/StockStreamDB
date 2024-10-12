import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from datetime import datetime
from src.infrastructure.db.stock_repository import (
    StockRepository,
)  # Updated import path


class TestStockRepository(unittest.TestCase):
    def setUp(self):
        self.repo = StockRepository()

    @patch("yfinance.Ticker")
    def test_get_stock_data_success(self, mock_ticker):
        # Mock stock data
        mock_stock_data = MagicMock()
        mock_stock_data.empty = False
        mock_stock_data.index = [datetime(2024, 1, 1)]
        mock_stock_data["Close"].iloc = MagicMock()
        # Set the value for iloc
        mock_stock_data["Close"].iloc.__getitem__.return_value = 155.0
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.return_value = mock_stock_data

        # Call the method
        result = self.repo.get_stock_data("AAPL")

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["close"], 155.0)
        self.assertEqual(result["date"], "2024-01-01")

    @patch("time.sleep", return_value=None)  # Mock sleep to speed up the test
    @patch("yfinance.Ticker")
    def test_get_stock_data_retry_success(self, mock_ticker, mock_sleep):
        # Simulate failure on the first attempt, success on the second
        mock_ticker_instance = mock_ticker.return_value
        mock_stock_data = MagicMock()
        mock_stock_data.empty = False
        mock_stock_data.index = [datetime(2024, 1, 1)]
        mock_stock_data["Close"].iloc = MagicMock()
        # Set the value for iloc
        mock_stock_data["Close"].iloc.__getitem__.return_value = 155.0

        mock_ticker_instance.history.side_effect = [
            RequestException("Connection error"),
            mock_stock_data,
        ]

        # Call the method
        result = self.repo.get_stock_data("AAPL", retries=2)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["close"], 155.0)
        self.assertEqual(result["date"], "2024-01-01")


if __name__ == "__main__":
    unittest.main()
