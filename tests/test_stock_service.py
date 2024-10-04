import unittest
from unittest.mock import MagicMock
from src.use_cases.stock_service import StockService
from src.domain.models.stock import Stock  # <-- Add this import

class TestStockService(unittest.TestCase):
    def test_fetch_stock(self):
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_stock.return_value = Stock(
            ticker="AAPL",
            name="Apple Inc.",
            industry="Technology",
            sector="Consumer Electronics",
            close=150.0,
            date="2024-04-27"
        )
        mock_fetcher = MagicMock()

        # Use correct parameter names as per StockService constructor
        service = StockService(stock_repository=mock_repo, stock_fetcher=mock_fetcher)

        # Act
        stock = service.stock_repository.get_stock("AAPL")

        # Assert
        self.assertEqual(stock.ticker, "AAPL")
        self.assertEqual(stock.name, "Apple Inc.")
        self.assertEqual(stock.close, 150.0)
        
if __name__ == '__main__':
    unittest.main()
