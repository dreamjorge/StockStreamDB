import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from io import StringIO
from src.application.generate_stock_data import (
    generate_stock_data,
    save_stock_data_to_csv,
)
import numpy as np
from datetime import datetime

# Helper function for DataFrame comparison


def assert_dataframes_equal(test_case, df1, df2):
    df1, df2 = df1.reset_index(drop=True), df2.reset_index(drop=True)
    pd.testing.assert_frame_equal(df1, df2)


# Helper function to create mock stock data with consistent dtypes


def create_mock_data(ticker, dates, prices):
    return pd.DataFrame(
        {"date": pd.to_datetime(dates), "ticker": ticker, "price": prices}
    )


# Helper function to get written CSV data and enforce datetime dtype on 'date'


def get_written_csv(mock_open_file):
    written_data = "".join(
        call.args[0] for call in mock_open_file().write.call_args_list
    )
    saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])
    saved_df["date"] = pd.to_datetime(
        saved_df["date"], errors="coerce"
    )  # Ensure datetime dtype
    saved_df["price"] = saved_df["price"].astype(
        "float64"
    )  # Force float64 dtype for consistency
    return saved_df


class TestGenerateStockData(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2023, 1, 5)
        self.output_file = "mock_stock_data.csv"

    @patch("builtins.open", new_callable=mock_open)
    @patch("src.application.generate_stock_data.generate_stock_data")
    def test_save_stock_data_to_csv(self, mock_generate, mock_open_file):
        tickers = ["NVDA", "AAPL"]
        mock_data = {
            "NVDA": create_mock_data(
                "NVDA",
                pd.date_range(self.start_date, periods=4),
                [100.0, 101.0, 102.0, 103.0],
            ),
            "AAPL": create_mock_data(
                "AAPL",
                pd.date_range(self.start_date, periods=4),
                [150.0, 151.0, 152.0, 153.0],
            ),
        }
        mock_generate.side_effect = [mock_data["NVDA"], mock_data["AAPL"]]

        save_stock_data_to_csv(
            tickers, self.start_date, self.end_date, self.output_file
        )

        saved_df = get_written_csv(mock_open_file)
        expected_df = pd.concat(
            [mock_data[ticker] for ticker in tickers], ignore_index=True
        )
        assert_dataframes_equal(self, saved_df, expected_df)

    @patch("numpy.random.normal")
    def test_generate_stock_data_deterministic_prices(self, mock_normal):
        ticker = "TEST"
        mock_normal.return_value = np.array([0.5, 0.5, 0.5, 0.5])
        expected_prices = np.cumsum([0.5, 0.5, 0.5, 0.5]) + 100
        expected_df = create_mock_data(
            ticker, pd.date_range(self.start_date, periods=4), expected_prices
        )

        result_df = generate_stock_data(ticker, self.start_date, self.end_date)
        assert_dataframes_equal(self, result_df, expected_df)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_empty_tickers(self, mock_open_file):
        save_stock_data_to_csv([], self.start_date, self.end_date, self.output_file)
        handle = mock_open_file()
        handle.write.assert_called_once_with("date,ticker,price\n")

    @patch("src.application.generate_stock_data.generate_stock_data")
    def test_generate_stock_data_empty_date_range(self, mock_generate):
        result_df = generate_stock_data("TEST", self.start_date, self.start_date)
        expected_df = create_mock_data("TEST", pd.to_datetime([]), [])
        assert_dataframes_equal(self, result_df, expected_df)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_single_ticker(self, mock_open_file):
        ticker = "AAPL"
        mock_data = create_mock_data(
            ticker,
            pd.date_range(self.start_date, periods=4),
            [150.0, 151.0, 152.0, 153.0],
        )

        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            return_value=mock_data,
        ):
            save_stock_data_to_csv(
                [ticker], self.start_date, self.end_date, self.output_file
            )

        saved_df = get_written_csv(mock_open_file)
        assert_dataframes_equal(self, saved_df, mock_data)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_invalid_date_range(self, mock_open_file):
        tickers = ["AAPL"]
        start_date, end_date = datetime(2023, 1, 5), datetime(2023, 1, 1)

        mock_data = create_mock_data("AAPL", pd.to_datetime([]), [])
        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            return_value=mock_data,
        ):
            save_stock_data_to_csv(tickers, start_date, end_date, self.output_file)

        saved_df = get_written_csv(mock_open_file)
        assert_dataframes_equal(self, saved_df, mock_data)


if __name__ == "__main__":
    unittest.main()
