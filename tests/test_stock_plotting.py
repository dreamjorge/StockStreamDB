# tests/test_stock_plotting.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.utils.stock_plotting import plot_stock_prices


class TestStockPlotting(unittest.TestCase):
    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices(self, mock_read_csv, mock_px_line):
        """Test the plot_stock_prices function with valid data."""
        # Arrange
        csv_file = "dummy_stock_data.csv"
        ticker = "AAPL"

        # Create a mock DataFrame
        mock_df = pd.DataFrame(
            {
                "ticker": ["AAPL", "AAPL", "MSFT"],
                "date": ["2023-01-01", "2023-01-02", "2023-01-01"],
                "price": [150, 152, 250],
            }
        )
        mock_read_csv.return_value = mock_df

        # Create a mock Plotly figure
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig

        # Act
        plot_stock_prices(csv_file, ticker)

        # Assert
        # Verify read_csv was called with the correct file
        mock_read_csv.assert_called_once_with(csv_file)

        # Verify px.line was called with the filtered DataFrame and correct parameters
        filtered_df = mock_df[mock_df["ticker"] == ticker]
        mock_px_line.assert_called_once()
        args, kwargs = mock_px_line.call_args

        # Use pandas testing to compare DataFrames
        pd.testing.assert_frame_equal(args[0], filtered_df)

        # Check other keyword arguments
        self.assertEqual(kwargs["x"], "date")
        self.assertEqual(kwargs["y"], "price")
        self.assertEqual(kwargs["title"], f"{ticker} Stock Prices (1 Year)")
        self.assertEqual(kwargs["labels"], {"date": "Date", "price": "Price"})

        # Verify update_layout was called with correct parameters
        mock_fig.update_layout.assert_called_once_with(
            xaxis_title="Date", yaxis_title="Price", template="plotly_dark"
        )

        # Verify show was called to display the plot
        mock_fig.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_invalid_csv(self, mock_read_csv, mock_px_line):
        """Test the plot_stock_prices function with an invalid CSV structure."""
        # Arrange
        csv_file = "invalid_stock_data.csv"
        ticker = "AAPL"

        # Create a mock DataFrame with missing 'price' column
        mock_df = pd.DataFrame(
            {
                "ticker": ["AAPL", "AAPL", "MSFT"],
                "date": ["2023-01-01", "2023-01-02", "2023-01-01"],
                # 'price' column is missing
            }
        )
        mock_read_csv.return_value = mock_df

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            plot_stock_prices(csv_file, ticker)

        # Optionally, check the error message
        self.assertIn("Missing columns in CSV: price", str(context.exception))

        # Verify read_csv was called with the correct file
        mock_read_csv.assert_called_once_with(csv_file)

        # Verify px.line was not called due to the exception
        mock_px_line.assert_not_called()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_no_data(self, mock_read_csv, mock_px_line):
        """Test the plot_stock_prices function when no data is found for the ticker."""
        # Arrange
        csv_file = "dummy_stock_data.csv"
        ticker = "GOOGL"

        # Create a mock DataFrame with no matching ticker
        mock_df = pd.DataFrame(
            {
                "ticker": ["AAPL", "AAPL", "MSFT"],
                "date": ["2023-01-01", "2023-01-02", "2023-01-01"],
                "price": [150, 152, 250],
            }
        )
        mock_read_csv.return_value = mock_df

        # Create a mock Plotly figure
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig

        # Act
        plot_stock_prices(csv_file, ticker)

        # Assert
        # Verify read_csv was called with the correct file
        mock_read_csv.assert_called_once_with(csv_file)

        # Verify px.line was called with the empty filtered DataFrame and correct
        # parameters
        filtered_df = mock_df[mock_df["ticker"] == ticker]
        mock_px_line.assert_called_once()
        args, kwargs = mock_px_line.call_args

        # Use pandas testing to compare DataFrames
        pd.testing.assert_frame_equal(args[0], filtered_df)

        # Check other keyword arguments
        self.assertEqual(kwargs["x"], "date")
        self.assertEqual(kwargs["y"], "price")
        self.assertEqual(kwargs["title"], f"{ticker} Stock Prices (1 Year)")
        self.assertEqual(kwargs["labels"], {"date": "Date", "price": "Price"})

        # Verify update_layout was called with correct parameters
        mock_fig.update_layout.assert_called_once_with(
            xaxis_title="Date", yaxis_title="Price", template="plotly_dark"
        )

        # Verify show was called to display the plot
        mock_fig.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_empty_csv(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with an empty CSV file."""
        # Arrange
        csv_file = "empty_stock_data.csv"
        ticker = "AAPL"

        # Empty DataFrame mock
        mock_df = pd.DataFrame(columns=["ticker", "date", "price"])
        mock_read_csv.return_value = mock_df

        # Act
        plot_stock_prices(csv_file, ticker)

        # Assert
        mock_read_csv.assert_called_once_with(csv_file)

        # Check if px.line was called with an empty filtered DataFrame
        args, kwargs = mock_px_line.call_args
        pd.testing.assert_frame_equal(args[0], mock_df[mock_df["ticker"] == ticker])

        # Check additional keyword arguments
        self.assertEqual(kwargs["x"], "date")
        self.assertEqual(kwargs["y"], "price")
        self.assertEqual(kwargs["title"], f"{ticker} Stock Prices (1 Year)")
        self.assertEqual(kwargs["labels"], {"date": "Date", "price": "Price"})

        # Verify show was called to display the plot
        mock_px_line.return_value.show.assert_called_once()

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_with_extra_columns(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices function with extra columns in CSV."""
        # Arrange
        csv_file = "extra_columns_stock_data.csv"
        ticker = "AAPL"

        # Mock DataFrame with extra columns
        mock_df = pd.DataFrame(
            {
                "ticker": ["AAPL", "AAPL", "MSFT"],
                "date": ["2023-01-01", "2023-01-02", "2023-01-01"],
                "price": [150, 152, 250],
                "volume": [1000, 1100, 1200],  # Extra column
            }
        )
        mock_read_csv.return_value = mock_df

        # Act
        plot_stock_prices(csv_file, ticker)

        # Assert
        mock_read_csv.assert_called_once_with(csv_file)
        filtered_df = mock_df[mock_df["ticker"] == ticker]

        # Use pd.testing.assert_frame_equal for DataFrame comparison
        args, kwargs = mock_px_line.call_args
        pd.testing.assert_frame_equal(args[0], filtered_df)
        self.assertEqual(kwargs["x"], "date")
        self.assertEqual(kwargs["y"], "price")
        self.assertEqual(kwargs["title"], f"{ticker} Stock Prices (1 Year)")
        self.assertEqual(kwargs["labels"], {"date": "Date", "price": "Price"})
        mock_px_line.return_value.show.assert_called

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_date_format_edge_case(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices with edge case date formats."""
        # Arrange
        csv_file = "edge_case_date_stock_data.csv"
        ticker = "AAPL"

        # Mock DataFrame with different date formats
        mock_df = pd.DataFrame(
            {
                "ticker": ["AAPL", "AAPL", "AAPL"],
                "date": ["01-01-2023", "2023/01/02", "Jan 03, 2023"],
                "price": [150, 152, 155],
            }
        )
        mock_read_csv.return_value = mock_df

        # Act
        plot_stock_prices(csv_file, ticker)

        # Assert
        mock_read_csv.assert_called_once_with(csv_file)

        # Retrieve the actual call arguments from mock_px_line
        args, kwargs = mock_px_line.call_args

        # Use pd.testing.assert

    @patch("src.utils.stock_plotting.px.line")
    @patch("src.utils.stock_plotting.pd.read_csv")
    def test_plot_stock_prices_with_duplicate_dates(self, mock_read_csv, mock_px_line):
        """Test plot_stock_prices function with duplicate dates for the same ticker."""
        # Arrange
        csv_file = "duplicate_dates_stock_data.csv"
        ticker = "AAPL"

        # Mock DataFrame with duplicate dates for the same ticker
        mock_df = pd.DataFrame(
            {
                "ticker": ["AAPL", "AAPL", "AAPL"],
                "date": ["2023-01-01", "2023-01-01", "2023-01-02"],
                "price": [150, 151, 152],
            }
        )
        mock_read_csv.return_value = mock_df

        # Act
        with self.assertRaises(ValueError) as context:
            plot_stock_prices(csv_file, ticker)

        # Assert
        # Verify read_csv was called with the correct file
        mock_read_csv.assert_called_once_with(csv_file)

        # Optionally, check the error message
        self.assertIn(
            "Duplicate dates found in data for ticker", str(context.exception)
        )

        # Verify px.line was not called due to the exception
        mock_px_line.assert_not_called()


if __name__ == "__main__":
    unittest.main()
