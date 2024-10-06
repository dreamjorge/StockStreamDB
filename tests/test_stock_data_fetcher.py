# tests/test_stock_data_fetcher.py

from unittest.mock import patch
import pandas as pd
from stock_data_fetcher import YahooFinanceFetcher  # Adjust import as per your script


def test_fetch_intraday_data():
    # Mock data
    index = pd.date_range(start="2021-01-01", periods=5, freq="min", name="Datetime")
    data = {
        "Open": [100, 101, 102, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Close": [102, 103, 104, 105, 106],
        "Adj Close": [102, 103, 104, 105, 106],  # Add this line
        "Volume": [1000, 1100, 1200, 1300, 1400],
    }
    df_mock = pd.DataFrame(data, index=index)

    with patch("yfinance.download", return_value=df_mock) as mock_download:
        fetcher = YahooFinanceFetcher()
        df = fetcher.fetch_intraday_data("TEST")

        # Assertions
        assert not df.empty, "DataFrame should not be empty."
        assert len(df) == 5, "DataFrame should have 5 rows."
        expected_columns = [
            "Datetime",
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]
        actual_columns = list(df.columns)
        assert (
            actual_columns == expected_columns
        ), f"Columns should match. Expected: {expected_columns}, Got: {actual_columns}"

        # Remove any extra columns like 'Adj Close' for comparison if not required
        df_clean = df[["Datetime", "Open", "High", "Low", "Close", "Volume"]]
        df_mock_clean = df_mock.reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]

        # Verify data equality
        pd.testing.assert_frame_equal(df_clean, df_mock_clean)

        # Check that the mock was called
        mock_download.assert_called_once_with(
            "TEST", interval="1m"
        )  # Adjust the arguments if necessary
