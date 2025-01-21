from abc import ABC, abstractmethod
from .Stock_Class import Stock_Class
from stock.models import Stock, StockData, Strategies, Recommendations

class Strategy(ABC):
    def __init__(self, ticker):
        self.signal = ""
        
        # Get the Stocks close prices from db
        self.ticker = ticker
        stock_object = Stock_Class(self.ticker)
        stock_field = StockData.objects.get(ticker=self.ticker)
        self.stats = stock_field.last_200_close_prices
        self.price = stock_field.current_price
        
    @abstractmethod
    def generate_signal(self):
        pass
    
    @abstractmethod
    def apply_strategy(self):
        pass