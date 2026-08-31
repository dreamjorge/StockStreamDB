import unittest
from datetime import date
from unittest.mock import MagicMock

import pandas as pd

from src.infrastructure.db.macro_repository_impl import MacroRepositoryImpl


class TestMacroRepositoryImpl(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repo = MacroRepositoryImpl(self.session)

    def test_save_series_adds_new_observations(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {"date": pd.to_datetime(["2024-01-01", "2024-02-01"]), "value": [5.25, 5.5]}
        )

        self.repo.save_series("FEDFUNDS", frame)

        self.assertEqual(self.session.add.call_count, 2)
        self.session.commit.assert_called_once()

    def test_save_series_updates_existing_observation_value(self):
        existing = MagicMock(value=1.0, date=date(2024, 1, 1))
        self.session.query.return_value.filter_by.return_value.all.return_value = [
            existing
        ]
        frame = pd.DataFrame({"date": pd.to_datetime(["2024-01-01"]), "value": [5.25]})

        self.repo.save_series("FEDFUNDS", frame)

        self.assertEqual(existing.value, 5.25)
        self.session.add.assert_not_called()
        self.session.commit.assert_called_once()

    def test_save_series_stores_plain_date_not_timestamp(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame({"date": pd.to_datetime(["2024-01-01"]), "value": [5.25]})

        self.repo.save_series("FEDFUNDS", frame)

        added = self.session.add.call_args[0][0]
        self.assertEqual(added.date, date(2024, 1, 1))

    def test_save_series_upserts_duplicate_dates_within_the_same_frame(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
                "value": [5.25, 5.50],
            }
        )

        self.repo.save_series("FEDFUNDS", frame)

        self.assertEqual(self.session.add.call_count, 1)
        added = self.session.add.call_args[0][0]
        self.assertEqual(added.value, 5.50)
        self.session.commit.assert_called_once()

    def test_save_series_loads_existing_observations_once_per_call(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
                "value": [5.25, 5.5, 5.5],
            }
        )

        self.repo.save_series("FEDFUNDS", frame)

        self.session.query.return_value.filter_by.assert_called_once_with(
            series_id="FEDFUNDS"
        )

    def test_get_series_queries_by_series_id_ordered_by_date(self):
        self.repo.get_series("FEDFUNDS")

        self.session.query.return_value.filter_by.assert_called_once_with(
            series_id="FEDFUNDS"
        )
        self.session.query.return_value.filter_by.return_value.order_by.assert_called_once()

    def test_series_exists_returns_scalar_result(self):
        self.session.query.return_value.scalar.return_value = True

        result = self.repo.series_exists("FEDFUNDS")

        self.assertTrue(result)
