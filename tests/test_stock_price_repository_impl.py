import unittest
from datetime import date
from unittest.mock import MagicMock

import pandas as pd

from src.infrastructure.db.stock_price_repository_impl import StockPriceRepositoryImpl


class TestStockPriceRepositoryImpl(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repo = StockPriceRepositoryImpl(self.session)

    def test_save_prices_adds_new_rows(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-02", "2024-01-03"]),
                "open": [148.0, 150.0],
                "high": [151.0, 152.0],
                "low": [147.0, 149.0],
                "close": [150.0, 151.0],
                "volume": [1000000, 1100000],
            }
        )

        self.repo.save_prices("AAPL", frame)

        self.assertEqual(self.session.add.call_count, 2)
        self.session.commit.assert_called_once()

    def test_save_prices_updates_existing_row(self):
        existing = MagicMock(close=100.0, date=date(2024, 1, 2))
        self.session.query.return_value.filter_by.return_value.all.return_value = [
            existing
        ]
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-02"]),
                "open": [148.0],
                "high": [151.0],
                "low": [147.0],
                "close": [150.0],
                "volume": [1000000],
            }
        )

        self.repo.save_prices("AAPL", frame)

        self.assertEqual(existing.close, 150.0)
        self.session.add.assert_not_called()
        self.session.commit.assert_called_once()

    def test_save_prices_stores_plain_date_not_timestamp(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-02"]),
                "open": [148.0],
                "high": [151.0],
                "low": [147.0],
                "close": [150.0],
                "volume": [1000000],
            }
        )

        self.repo.save_prices("AAPL", frame)

        added = self.session.add.call_args[0][0]
        self.assertEqual(added.date, date(2024, 1, 2))

    def test_save_prices_upserts_duplicate_dates_within_the_same_frame(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-02", "2024-01-02"]),
                "open": [148.0, 149.0],
                "high": [151.0, 153.0],
                "low": [147.0, 148.0],
                "close": [150.0, 152.0],
                "volume": [1000000, 1200000],
            }
        )

        self.repo.save_prices("AAPL", frame)

        self.assertEqual(self.session.add.call_count, 1)
        added = self.session.add.call_args[0][0]
        self.assertEqual(added.close, 152.0)
        self.session.commit.assert_called_once()

    def test_save_prices_loads_existing_rows_once_per_call(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
                "open": [148.0, 150.0, 151.0],
                "high": [151.0, 152.0, 153.0],
                "low": [147.0, 149.0, 150.0],
                "close": [150.0, 151.0, 152.0],
                "volume": [1000000, 1100000, 1200000],
            }
        )

        self.repo.save_prices("AAPL", frame)

        self.session.query.return_value.filter_by.assert_called_once_with(ticker="AAPL")

    def test_save_prices_stores_adjusted_close_when_present(self):
        self.session.query.return_value.filter_by.return_value.all.return_value = []
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-02"]),
                "open": [148.0],
                "high": [151.0],
                "low": [147.0],
                "close": [150.0],
                "adjusted_close": [149.5],
                "volume": [1000000],
            }
        )

        self.repo.save_prices("AAPL", frame)

        added = self.session.add.call_args[0][0]
        self.assertEqual(added.adjusted_close, 149.5)

    def test_get_prices_queries_by_ticker_ordered_by_date(self):
        self.repo.get_prices("AAPL")

        self.session.query.return_value.filter_by.assert_called_once_with(ticker="AAPL")
        self.session.query.return_value.filter_by.return_value.order_by.assert_called_once()

    def test_exists_in_range_returns_scalar_result(self):
        self.session.query.return_value.scalar.return_value = True

        result = self.repo.exists_in_range("AAPL", date(2024, 1, 1), date(2024, 2, 1))

        self.assertTrue(result)
