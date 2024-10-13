import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import numpy as np
from datetime import datetime
from src.application.generate_stock_data import (
    generate_stock_data,
    save_stock_data_to_csv,
)


class TestGenerateStockData(unittest.TestCase):
    def test_generate_stock_data(self):
        ticker = "AAPL"
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 10)

        # Generate stock data
        stock_data = generate_stock_data(ticker, start_date, end_date)

        # Assert the number of rows equals the number of days in the range
        num_days = (end_date - start_date).days
        self.assertEqual(len(stock_data), num_days)

        # Assert that all tickers are the same
        self.assertTrue((stock_data["ticker"] == ticker).all())

        # Assert that the date range is correct
        expected_dates = pd.date_range(
            start=start_date, end=end_date - pd.Timedelta(days=1), freq="D"
        )
        pd.testing.assert_series_equal(stock_data["date"], pd.Series(expected_dates))

        # Assert that prices are floats
        self.assertTrue(np.issubdtype(stock_data["price"].dtype, np.floating))

    @patch("builtins.open", new_callable=mock_open)
    @patch("pandas.DataFrame.to_csv")
    def test_save_stock_data_to_csv(self, mock_to_csv, mock_open_file):
        tickers = ["NVDA", "AAPL"]
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 5)
        output_file = "mock_stock_data.csv"

        # Call the function to save stock data to CSV
        save_stock_data_to_csv(tickers, start_date, end_date, output_file)

        # Check that the DataFrame.to_csv() was called once
        mock_to_csv.assert_called_once_with(output_file, index=False)

        # Generate expected DataFrame for validation
        expected_data = pd.concat(
            [generate_stock_data(ticker, start_date, end_date) for ticker in tickers],
            ignore_index=True,
        )

        # Validate the contents of the DataFrame passed to to_csv
        pd.testing.assert_frame_equal(mock_to_csv.call_args[0][0], expected_data)


if __name__ == "__main__":
    unittest.main()
