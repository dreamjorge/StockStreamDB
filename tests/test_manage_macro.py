import unittest
from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.application.use_cases.manage_macro import ManageMacroUseCase


class TestManageMacroUseCase(unittest.TestCase):
    def setUp(self):
        self.macro_repo = MagicMock()
        self.macro_fetcher = MagicMock()
        self.use_case = ManageMacroUseCase(self.macro_repo, self.macro_fetcher)

    def test_fetch_and_store_series_saves_and_returns_count(self):
        frame = pd.DataFrame({"date": pd.to_datetime(["2024-01-01"]), "value": [5.25]})
        self.macro_fetcher.fetch.return_value = frame

        count = self.use_case.fetch_and_store_series("FEDFUNDS", start="2024-01-01")

        self.macro_fetcher.fetch.assert_called_once_with(
            "FEDFUNDS", start="2024-01-01", end=None
        )
        self.macro_repo.save_series.assert_called_once_with("FEDFUNDS", frame)
        self.assertEqual(count, 1)

    def test_fetch_and_store_series_returns_zero_for_no_data(self):
        self.macro_fetcher.fetch.return_value = None

        count = self.use_case.fetch_and_store_series("UNKNOWN")

        self.macro_repo.save_series.assert_not_called()
        self.assertEqual(count, 0)

    def test_fetch_and_store_series_requires_a_fetcher(self):
        use_case = ManageMacroUseCase(self.macro_repo)

        with pytest.raises(ValueError):
            use_case.fetch_and_store_series("FEDFUNDS")

    def test_series_exists_delegates_to_repository(self):
        self.macro_repo.series_exists.return_value = True

        result = self.use_case.series_exists("FEDFUNDS")

        self.macro_repo.series_exists.assert_called_once_with("FEDFUNDS")
        self.assertTrue(result)
