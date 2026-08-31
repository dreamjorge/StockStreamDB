"""FRED (Federal Reserve Economic Data) macro-indicator fetcher."""

import os

import pandas as pd
from fredapi import Fred


class FredFetcher:
    """Fetches macro-economic time series (interest rates, inflation, unemployment,
    etc.) from FRED. Requires a free API key from
    https://fred.stlouisfed.org/docs/api/api_key.html, passed explicitly or via the
    FRED_API_KEY environment variable.
    """

    def __init__(self, api_key=None):
        resolved_key = api_key or os.environ.get("FRED_API_KEY")
        if not resolved_key:
            raise ValueError(
                "FRED_API_KEY is required. Get a free key at "
                "https://fred.stlouisfed.org/docs/api/api_key.html and set it as the "
                "FRED_API_KEY environment variable, or pass api_key explicitly."
            )
        self.client = Fred(api_key=resolved_key)

    def fetch(self, series_id, start=None, end=None):
        """Fetch a FRED series and return a DataFrame with 'date' and 'value' columns,
        or None on error or if the series has no observations in range."""
        try:
            series = self.client.get_series(
                series_id, observation_start=start, observation_end=end
            )
        except Exception as e:
            print(f"Network error occurred: {e}")
            return None

        if series is None or series.empty:
            return None

        series = series.dropna()
        if series.empty:
            return None

        return (
            series.rename("value")
            .rename_axis("date")
            .reset_index()
            .assign(date=lambda df: pd.to_datetime(df["date"]))
        )
