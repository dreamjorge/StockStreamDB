# tests/test_generate_stock_data.py

import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from io import StringIO
from src.application.generate_stock_data import (
    generate_stock_data,
    save_stock_data_to_csv,
)
import numpy as np
import datetime


class TestGenerateStockData(unittest.TestCase):
    # Existing Tests
    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv(self, mock_open_file):
        tickers = ["NVDA", "AAPL"]
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 5)
        output_file = "mock_stock_data.csv"

        # Mock the output of generate_stock_data for both tickers
        mock_nvda_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=4),
                "ticker": "NVDA",
                "price": [100.0, 101.0, 102.0, 103.0],
            }
        )
        mock_aapl_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=4),
                "ticker": "AAPL",
                "price": [150.0, 151.0, 152.0, 153.0],
            }
        )

        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            side_effect=[mock_nvda_data, mock_aapl_data],
        ):
            # Call the function to save stock data to CSV
            save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Expected concatenated DataFrame
        expected_data = pd.concat([mock_nvda_data, mock_aapl_data], ignore_index=True)

        # Retrieve the file handle mock
        handle = mock_open_file()

        # Capture all write calls to the file
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Debug: Print the written CSV data
        print("Written CSV Data:")
        print(repr(written_data))

        # Convert the written CSV data back into a DataFrame
        saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])

        # Ensure columns are in the same order
        saved_df = saved_df[["date", "ticker", "price"]]
        expected_data = expected_data[["date", "ticker", "price"]]

        # Reset indexes
        saved_df = saved_df.reset_index(drop=True)
        expected_data = expected_data.reset_index(drop=True)

        # Ensure that the saved DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(saved_df, expected_data)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_multiple_tickers(self, mock_open_file):
        tickers = ["AAPL", "NVDA", "MSFT"]
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 3)
        output_file = "mock_stock_data.csv"

        # Mock the output of generate_stock_data for multiple tickers
        mock_aapl_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=2),
                "ticker": "AAPL",
                "price": [100.0, 101.0],
            }
        )
        mock_nvda_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=2),
                "ticker": "NVDA",
                "price": [110.0, 111.0],
            }
        )
        mock_msft_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=2),
                "ticker": "MSFT",
                "price": [120.0, 121.0],
            }
        )

        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            side_effect=[mock_aapl_data, mock_nvda_data, mock_msft_data],
        ):
            # Call the function to save stock data to CSV
            save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Expected concatenated DataFrame
        expected_data = pd.concat(
            [mock_aapl_data, mock_nvda_data, mock_msft_data], ignore_index=True
        )

        # Retrieve the file handle mock
        handle = mock_open_file()

        # Capture all write calls to the file
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Debug: Print the written CSV data
        print("Written CSV Data:")
        print(repr(written_data))

        # Convert the written CSV data back into a DataFrame
        saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])

        # Ensure columns are in the same order
        saved_df = saved_df[["date", "ticker", "price"]]
        expected_data = expected_data[["date", "ticker", "price"]]

        # Reset indexes
        saved_df = saved_df.reset_index(drop=True)
        expected_data = expected_data.reset_index(drop=True)

        # Ensure that the saved DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(saved_df, expected_data)

    # Additional Tests for Complete Coverage

    # Test generate_stock_data with empty date range (start_date == end_date)
    def test_generate_stock_data_empty_date_range(self):
        ticker = "TEST"
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 1)

        expected_df = pd.DataFrame(
            {
                "date": pd.Series([], dtype="datetime64[ns]"),
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="float64"),
            }
        )

        result_df = generate_stock_data(ticker, start_date, end_date)

        # Ensure columns are in the same order
        result_df = result_df[["date", "ticker", "price"]]
        expected_df = expected_df[["date", "ticker", "price"]]

        # Reset indexes
        result_df = result_df.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)

        pd.testing.assert_frame_equal(result_df, expected_df)

    # Test generate_stock_data with start_date after end_date
    def test_generate_stock_data_invalid_date_range(self):
        ticker = "TEST"
        start_date = datetime(2023, 1, 5)
        end_date = datetime(2023, 1, 1)

        expected_df = pd.DataFrame(
            {
                "date": pd.Series([], dtype="datetime64[ns]"),
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="float64"),
            }
        )

        result_df = generate_stock_data(ticker, start_date, end_date)

        # Ensure columns are in the same order
        result_df = result_df[["date", "ticker", "price"]]
        expected_df = expected_df[["date", "ticker", "price"]]

        # Reset indexes
        result_df = result_df.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)

        pd.testing.assert_frame_equal(result_df, expected_df)

    # Test save_stock_data_to_csv with empty tickers list
    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_empty_tickers(self, mock_open_file):
        tickers = []
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 5)
        output_file = "mock_stock_data.csv"

        # Since tickers are empty, generate_stock_data should not be called
        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            return_value=pd.DataFrame(columns=["date", "ticker", "price"]),
        ) as mock_generate:
            # Call the function to save stock data to CSV
            save_stock_data_to_csv(tickers, start_date, end_date, output_file)
            mock_generate.assert_not_called()

        # Expected DataFrame is empty with 'date' as object dtype
        expected_data = pd.DataFrame(
            {
                "date": pd.Series([], dtype="object"),  # Changed to 'object'
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="object"),  # Changed to 'object'
            }
        )

        # Retrieve the file handle mock
        handle = mock_open_file()

        # Capture all write calls to the file
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Debug: Print the written CSV data
        print("Written CSV Data:")
        print(repr(written_data))

        # Convert the written CSV data back into a DataFrame
        saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])

        # Ensure columns are in the same order
        saved_df = saved_df[["date", "ticker", "price"]]
        expected_data = expected_data[["date", "ticker", "price"]]

        # Reset indexes
        saved_df = saved_df.reset_index(drop=True)
        expected_data = expected_data.reset_index(drop=True)

        # Ensure that the saved DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(saved_df, expected_data)

    # Test save_stock_data_to_csv with single ticker
    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_single_ticker(self, mock_open_file):
        tickers = ["AAPL"]
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 4)
        output_file = "mock_stock_data.csv"

        # Mock the output of generate_stock_data for single ticker
        mock_aapl_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=3),
                "ticker": "AAPL",
                "price": [150.0, 151.0, 152.0],
            }
        )

        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            return_value=mock_aapl_data,
        ):
            # Call the function to save stock data to CSV
            save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Expected DataFrame
        expected_data = mock_aapl_data

        # Ensure columns are in the same order
        expected_data = expected_data[["date", "ticker", "price"]]
        saved_df = pd.read_csv(
            StringIO("date,ticker,price\n"), parse_dates=["date"]
        )  # Adjusted for empty

        # Retrieve the file handle mock
        handle = mock_open_file()

        # Capture all write calls to the file
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Debug: Print the written CSV data
        print("Written CSV Data:")
        print(repr(written_data))

        # Convert the written CSV data back into a DataFrame
        saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])

        # Ensure columns are in the same order
        saved_df = saved_df[["date", "ticker", "price"]]
        expected_data = expected_data[["date", "ticker", "price"]]

        # Reset indexes
        saved_df = saved_df.reset_index(drop=True)
        expected_data = expected_data.reset_index(drop=True)

        # Ensure that the saved DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(saved_df, expected_data)

    # Test save_stock_data_to_csv with start_date == end_date
    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_same_start_end_date(self, mock_open_file):
        tickers = ["AAPL"]
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 1)
        output_file = "mock_stock_data.csv"

        # Mock the output of generate_stock_data for single ticker with empty date range
        mock_aapl_data = pd.DataFrame(
            {
                "date": pd.Series([], dtype="datetime64[ns]"),
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="object"),  # Changed to 'object'
            }
        )

        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            return_value=mock_aapl_data,
        ):
            # Call the function to save stock data to CSV
            save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Expected DataFrame is empty with 'date' as object dtype
        expected_data = pd.DataFrame(
            {
                "date": pd.Series([], dtype="object"),  # Changed to 'object'
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="object"),  # Changed to 'object'
            }
        )

        # Retrieve the file handle mock
        handle = mock_open_file()

        # Capture all write calls to the file
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Debug: Print the written CSV data
        print("Written CSV Data:")
        print(repr(written_data))

        # Convert the written CSV data back into a DataFrame
        # An empty DataFrame with columns will result in a header only in CSV
        saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])

        # Ensure columns are in the same order
        saved_df = saved_df[["date", "ticker", "price"]]
        expected_data = expected_data[["date", "ticker", "price"]]

        # Reset indexes
        saved_df = saved_df.reset_index(drop=True)
        expected_data = expected_data.reset_index(drop=True)

        # Ensure that the saved DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(saved_df, expected_data)

    # Test save_stock_data_to_csv with start_date after end_date
    @patch("builtins.open", new_callable=mock_open)
    def test_save_stock_data_to_csv_start_date_after_end_date(self, mock_open_file):
        tickers = ["AAPL"]
        start_date = datetime(2023, 1, 5)
        end_date = datetime(2023, 1, 1)
        output_file = "mock_stock_data.csv"

        # Mock the output of generate_stock_data for single ticker with invalid
        # date range
        mock_aapl_data = pd.DataFrame(
            {
                "date": pd.Series([], dtype="datetime64[ns]"),
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="object"),  # Changed to 'object'
            }
        )

        with patch(
            "src.application.generate_stock_data.generate_stock_data",
            return_value=mock_aapl_data,
        ):
            # Call the function to save stock data to CSV
            save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Expected DataFrame is empty with 'date' as object dtype
        expected_data = pd.DataFrame(
            {
                "date": pd.Series([], dtype="object"),  # Changed to 'object'
                "ticker": pd.Series([], dtype="object"),
                "price": pd.Series([], dtype="object"),  # Changed to 'object'
            }
        )

        # Retrieve the file handle mock
        handle = mock_open_file()

        # Capture all write calls to the file
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Debug: Print the written CSV data
        print("Written CSV Data:")
        print(repr(written_data))

        # Convert the written CSV data back into a DataFrame
        saved_df = pd.read_csv(StringIO(written_data), parse_dates=["date"])

        # Ensure columns are in the same order
        saved_df = saved_df[["date", "ticker", "price"]]
        expected_data = expected_data[["date", "ticker", "price"]]

        # Reset indexes
        saved_df = saved_df.reset_index(drop=True)
        expected_data = expected_data.reset_index(drop=True)

        # Ensure that the saved DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(saved_df, expected_data)

    # Test generate_stock_data with invalid ticker type (e.g., integer)
    def test_generate_stock_data_invalid_ticker_type(self):
        ticker = 123  # Non-string ticker
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 5)

        # Depending on implementation, this might raise an error or handle gracefully
        # Since the current implementation does not enforce ticker type, it will proceed
        result_df = generate_stock_data(ticker, start_date, end_date)

        expected_dates = pd.date_range(start="2023-01-01", periods=4)
        # expected_prices = (
        #     np.cumsum([0.5, 0.5, 0.5, 0.5]) + 100
        # )  # Assuming deterministic walk

        self.assertEqual(len(result_df), 4)
        self.assertListEqual(list(result_df["ticker"]), [ticker] * 4)
        self.assertListEqual(result_df["date"].tolist(), list(expected_dates))
        # Note: Since random data is involved, consider mocking
        # numpy.random.normal for deterministic tests

    # Test that save_stock_data_to_csv calls generate_stock_data with correct parameters
    @patch("builtins.open", new_callable=mock_open)
    @patch("src.application.generate_stock_data.generate_stock_data")
    def test_save_stock_data_calls_generate_stock_data_with_correct_parameters(
        self, mock_generate, mock_open_file
    ):
        tickers = ["AAPL", "NVDA"]
        start_date = datetime(2023, 2, 1)
        end_date = datetime(2023, 2, 5)
        output_file = "mock_stock_data.csv"

        # Setup mock return values
        mock_aapl_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-02-01", periods=4),
                "ticker": "AAPL",
                "price": [150.0, 151.0, 152.0, 153.0],
            }
        )
        mock_nvda_data = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-02-01", periods=4),
                "ticker": "NVDA",
                "price": [200.0, 201.0, 202.0, 203.0],
            }
        )
        mock_generate.side_effect = [mock_aapl_data, mock_nvda_data]

        # Call the function
        save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Assert generate_stock_data was called correctly
        expected_calls = [
            unittest.mock.call("AAPL", start_date, end_date),
            unittest.mock.call("NVDA", start_date, end_date),
        ]
        self.assertEqual(mock_generate.call_args_list, expected_calls)

    # Test generate_stock_data price generation with deterministic random walk
    @patch("numpy.random.normal")
    def test_generate_stock_data_deterministic_prices(self, mock_normal):
        ticker = "TEST"
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 5)

        # Setup deterministic random values
        mock_normal.return_value = np.array([0.5, 0.5, 0.5, 0.5])

        expected_prices = (
            np.cumsum([0.5, 0.5, 0.5, 0.5]) + 100
        )  # [100.5, 101.0, 101.5, 102.0]

        expected_df = pd.DataFrame(
            {
                "date": pd.date_range(start="2023-01-01", periods=4),
                "ticker": "TEST",
                "price": expected_prices,
            }
        )

        result_df = generate_stock_data(ticker, start_date, end_date)

        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == "__main__":
    unittest.main()
