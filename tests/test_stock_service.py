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
        service = StockService(repository=mock_repo)

        # Act
        stock = service.fetch_stock("AAPL")

        # Assert
        self.assertEqual(stock.name, "Apple Inc.")
        mock_repo.get_stock.assert_called_once_with("AAPL")

if __name__ == '__main__':
    unittest.main()
