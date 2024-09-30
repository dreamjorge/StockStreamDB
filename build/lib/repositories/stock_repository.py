from abc import ABC, abstractmethod
from src.domain.models.stock import Stock

class StockRepository(ABC):

    @abstractmethod
    def create_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def delete_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def get(self, ticker: str) -> Stock:
        
pass/*************  ✨ Codeium Command ⭐  *************/
        """Fetches a stock by its ticker symbol.

        Args:
            ticker: The ticker symbol of the stock to fetch.

        Returns:
            The stock with the given ticker symbol, or None if no such stock exists.
        """

/******  1caa5147-b513-484f-9b1b-088a2ed9ebba  *******/

    @abstractmethod
    def update(self, stock: Stock) -> Stock:
        pass


    @abstractmethod
    def save(self, stock):
        pass
    
    @abstractmethod
    def get_by_ticker(self, ticker: str, granularity: Granularity = Granularity.DAILY) -> Stock:
        """
        Fetch stock data by ticker with a specified granularity (daily, weekly, etc.).
        """
        pass
    
    @abstractmethod
    def get_stock_data(self, ticker, start_date, end_date, granularity=Granularity.DAILY):
        pass

