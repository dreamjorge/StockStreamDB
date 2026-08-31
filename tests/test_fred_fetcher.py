import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from src.infrastructure.fetchers.fred_fetcher import FredFetcher


class TestFredFetcher(unittest.TestCase):
    def test_raises_without_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError):
                FredFetcher()

    def test_uses_api_key_argument_over_environment(self):
        with patch.dict("os.environ", {"FRED_API_KEY": "env-key"}, clear=True):
            with patch("src.infrastructure.fetchers.fred_fetcher.Fred") as mock_fred:
                FredFetcher(api_key="explicit-key")
                mock_fred.assert_called_once_with(api_key="explicit-key")

    def test_uses_environment_variable_when_no_argument_given(self):
        with patch.dict("os.environ", {"FRED_API_KEY": "env-key"}, clear=True):
            with patch("src.infrastructure.fetchers.fred_fetcher.Fred") as mock_fred:
                FredFetcher()
                mock_fred.assert_called_once_with(api_key="env-key")

    def test_fetch_returns_date_value_dataframe(self):
        with patch("src.infrastructure.fetchers.fred_fetcher.Fred") as mock_fred_class:
            mock_client = MagicMock()
            mock_client.get_series.return_value = pd.Series(
                [5.25, 5.5], index=pd.to_datetime(["2024-01-01", "2024-02-01"])
            )
            mock_fred_class.return_value = mock_client

            fetcher = FredFetcher(api_key="key")
            result = fetcher.fetch("FEDFUNDS", start="2024-01-01", end="2024-02-01")

            mock_client.get_series.assert_called_once_with(
                "FEDFUNDS", observation_start="2024-01-01", observation_end="2024-02-01"
            )
            self.assertEqual(list(result.columns), ["date", "value"])
            self.assertEqual(result["value"].tolist(), [5.25, 5.5])

    def test_fetch_returns_none_for_empty_series(self):
        with patch("src.infrastructure.fetchers.fred_fetcher.Fred") as mock_fred_class:
            mock_client = MagicMock()
            mock_client.get_series.return_value = pd.Series([], dtype="float64")
            mock_fred_class.return_value = mock_client

            fetcher = FredFetcher(api_key="key")
            result = fetcher.fetch("UNKNOWN")

            self.assertIsNone(result)

    def test_fetch_returns_none_on_network_error(self):
        with patch("src.infrastructure.fetchers.fred_fetcher.Fred") as mock_fred_class:
            mock_client = MagicMock()
            mock_client.get_series.side_effect = Exception("boom")
            mock_fred_class.return_value = mock_client

            fetcher = FredFetcher(api_key="key")
            result = fetcher.fetch("FEDFUNDS")

            self.assertIsNone(result)

    def test_fetch_drops_missing_observations(self):
        with patch("src.infrastructure.fetchers.fred_fetcher.Fred") as mock_fred_class:
            mock_client = MagicMock()
            mock_client.get_series.return_value = pd.Series(
                [5.25, None, 5.75],
                index=pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
            )
            mock_fred_class.return_value = mock_client

            fetcher = FredFetcher(api_key="key")
            result = fetcher.fetch("FEDFUNDS")

            self.assertEqual(result["value"].tolist(), [5.25, 5.75])
