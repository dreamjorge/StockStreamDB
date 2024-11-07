import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.utils.stock_plotting import plot_stock_prices


class TestStockPlotting(unittest.TestCase):

    def setUp(self):
        self.csv_file = "dummy_stock_data.csv"
        self.ticker = "AAPL"

    def create_mock_data(self, tickers, dates, prices):
        """Helper to create a mock DataFrame."""
        return pd.DataFrame({"ticker": tickers, "date": dates, "price": prices})

    def assert_plot_called_with(self, mock_px_line, df, title):
        """Helper to verify plot function was called with the correct parameters."""
        mock_px_line.assert_called_once()
        args, kwargs = mock_px_line.call_args
        pd.testing.assert_frame_equal(args[0], df)
        self.assertEqual(kwargs["x"], "date")
        self.assertEqual(kwargs["y"], "price")
        self.assertEqual(kwargs["title"], title)
        self.assertEqual(kwargs["labels"], {"date": "Date", "price": "Price"})

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with valid data."""
        mock_df = self.create_mock_data(
            ["AAPL", "AAPL", "MSFT"],
            ["2023-01-01", "2023-01-02", "2023-01-01"],
            [150, 152, 250],
        )
        mock_read_csv.return_value = mock_df
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig

        plot_stock_prices(self.csv_file, self.ticker)

        mock_read_csv.assert_called_once_with(self.csv_file)
        self.assert_plot_called_with(
            mock_px_line,
            mock_df[mock_df["ticker"] == self.ticker],
            f"{self.ticker} Stock Prices (1 Year)",
        )
        mock_fig.update_layout.assert_called_once_with(
            xaxis_title="Date", yaxis_title="Price", template="plotly_dark"
        )
        mock_fig.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_invalid_csv(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with missing columns."""
        mock_df = pd.DataFrame({"ticker": ["AAPL"], "date": ["2023-01-01"]})
        mock_read_csv.return_value = mock_df

        with self.assertRaises(ValueError) as context:
            plot_stock_prices(self.csv_file, self.ticker)

        self.assertIn("Missing columns in CSV", str(context.exception))
        mock_read_csv.assert_called_once_with(self.csv_file)
        mock_px_line.assert_not_called()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_no_data(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with no matching ticker data."""
        mock_df = self.create_mock_data(
            ["AAPL", "MSFT"], ["2023-01-01", "2023-01-01"], [150, 250]
        )
        mock_read_csv.return_value = mock_df
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig

        plot_stock_prices(self.csv_file, "GOOGL")

        mock_read_csv.assert_called_once_with(self.csv_file)
        self.assert_plot_called_with(
            mock_px_line,
            mock_df[mock_df["ticker"] == "GOOGL"],
            "GOOGL Stock Prices (1 Year)",
        )
        mock_fig.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_empty_csv(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with an empty CSV file."""
        mock_df = pd.DataFrame(columns=["ticker", "date", "price"])
        mock_read_csv.return_value = mock_df
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig

        plot_stock_prices(self.csv_file, self.ticker)

        mock_read_csv.assert_called_once_with(self.csv_file)
        self.assert_plot_called_with(
            mock_px_line,
            mock_df[mock_df["ticker"] == self.ticker],
            f"{self.ticker} Stock Prices (1 Year)",
        )
        mock_fig.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_with_extra_columns(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with extra columns in the CSV."""
        mock_df = self.create_mock_data(
            ["AAPL", "AAPL", "MSFT"],
            ["2023-01-01", "2023-01-02", "2023-01-01"],
            [150, 152, 250],
        )
        mock_df["volume"] = [1000, 1100, 1200]
        mock_read_csv.return_value = mock_df
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig

        plot_stock_prices(self.csv_file, self.ticker)

        mock_read_csv.assert_called_once_with(self.csv_file)
        self.assert_plot_called_with(
            mock_px_line,
            mock_df[mock_df["ticker"] == self.ticker],
            f"{self.ticker} Stock Prices (1 Year)",
        )
        mock_fig.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_with_duplicate_dates(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with duplicate dates for the same ticker."""
        mock_df = self.create_mock_data(
            ["AAPL", "AAPL", "AAPL"],
            ["2023-01-01", "2023-01-01", "2023-01-02"],
            [150, 151, 152],
        )
        mock_read_csv.return_value = mock_df

        with self.assertRaises(ValueError) as context:
            plot_stock_prices(self.csv_file, self.ticker)

        self.assertIn(
            "Duplicate dates found in data for ticker", str(context.exception)
        )
        mock_read_csv.assert_called_once_with(self.csv_file)
        mock_px_line.assert_not_called()


if __name__ == "__main__":
    unittest.main()
