import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from datetime import datetime
from src.infrastructure.db.stock_repository import StockRepository


class TestStockRepository(unittest.TestCase):
    def setUp(self):
        self.repo = StockRepository()

    @patch("yfinance.Ticker")
    def test_get_stock_data_success(self, mock_ticker):
        # Mock successful stock data retrieval
        mock_stock_data = MagicMock()
        mock_stock_data.empty = False
        mock_stock_data.index = [datetime(2024, 1, 1)]
        mock_stock_data["Close"].iloc.__getitem__.return_value = 155.0
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.return_value = mock_stock_data

        result = self.repo.get_stock_data("AAPL")
        self.assertIsNotNone(result)
        self.assertEqual(result["close"], 155.0)
        self.assertEqual(result["date"], "2024-01-01")

    @patch("time.sleep", return_value=None)
    @patch("yfinance.Ticker")
    def test_get_stock_data_retry_success(self, mock_ticker, mock_sleep):
        # First attempt fails, second succeeds
        mock_stock_data = MagicMock()
        mock_stock_data.empty = False
        mock_stock_data.index = [datetime(2024, 1, 1)]
        mock_stock_data["Close"].iloc.__getitem__.return_value = 155.0
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.side_effect = [
            RequestException("Connection error"),
            mock_stock_data,
        ]

        result = self.repo.get_stock_data("AAPL", retries=2)
        self.assertIsNotNone(result)
        self.assertEqual(result["close"], 155.0)
        self.assertEqual(result["date"], "2024-01-01")

    @patch("yfinance.Ticker")
    def test_get_stock_data_empty_data(self, mock_ticker):
        # Empty stock data should return None
        mock_stock_data = MagicMock()
        mock_stock_data.empty = True
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.return_value = mock_stock_data

        result = self.repo.get_stock_data("AAPL")
        self.assertIsNone(result)

    @patch("yfinance.Ticker")
    def test_get_stock_data_value_error(self, mock_ticker):
        # Simulate a ValueError to test handling
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.side_effect = ValueError("Data parsing error")

        result = self.repo.get_stock_data("AAPL")
        self.assertIsNone(result)

    @patch("yfinance.Ticker")
    def test_get_stock_data_unexpected_exception(self, mock_ticker):
        # Simulate an unexpected exception
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.side_effect = Exception("Unexpected error")

        result = self.repo.get_stock_data("AAPL")
        self.assertIsNone(result)

    @patch("time.sleep", return_value=None)
    @patch("yfinance.Ticker")
    def test_get_stock_data_retry_limit_exceeded(self, mock_ticker, mock_sleep):
        # Exceed retry limit without success
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.side_effect = RequestException("Connection error")

        result = self.repo.get_stock_data("AAPL", retries=2)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
