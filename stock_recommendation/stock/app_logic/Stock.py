import yfinance as yf
import models.Stock
import models.StockData
import models.Recommendations
class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = None
        self.signals = {}
        self.recommendation = None
        
    def get_data(self):
        info = self.ticker.info()
        update_data(self, info)
    
    def update_data(self, info): # Make this work for the database record which is being updated
        # 'Stock' model
        Stock.ticker = ticker
        Stock.company_name = info['shortName']
        Stock.sector = info['sector']
        # 'StockData' model
        StockData.open_price = info['open']
        StockData.close_price = info['previousClose']
        StockData.high_price = info['dayHigh']
        StockData.low_price = info['dayLow']
        StockData.volume = info['volume']
    
    def calculate_moving_average(self):
        pass
    
    def calculate_RSI():
        pass
    
    def calculate_bollinger_bands(self):
        pass
    
    def add_indicator(self):
        # adds indicator to the indicators dict
        pass
    
    def make_recommendation(self):
        # makes recommendation based on indicators
        pass