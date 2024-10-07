import unittest
from src.domain.repositories.base_stock_repository import BaseStockRepository


class TestBaseStockRepository(unittest.TestCase):
    def setUp(self):
        self.repo = BaseStockRepository()

    def test_create_stock_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError) as context:
            self.repo.create_stock(None)
        self.assertEqual(
            str(context.exception), "create_stock must be implemented by subclasses"
        )

    def test_get_stock_by_ticker_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError) as context:
            self.repo.get_stock_by_ticker("AAPL")
        self.assertEqual(
            str(context.exception),
            "get_stock_by_ticker must be implemented by subclasses",
        )

    def test_update_stock_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError) as context:
            self.repo.update_stock(None)
        self.assertEqual(
            str(context.exception), "update_stock must be implemented by subclasses"
        )

    def test_delete_stock_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError) as context:
            self.repo.delete_stock(None)
        self.assertEqual(
            str(context.exception), "delete_stock must be implemented by subclasses"
        )


if __name__ == "__main__":
    unittest.main()
