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
        
    # Make this work for the database record which is being updated
    def update_data(self):
        info = self.ticker.info()
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
        #Ignore next 3 lines
        ######Below is alternate code############
        #global Stock_model_data = []
        #global StockData_model_data = []
    
    def add_indicator(self):
        # adds indicator to the indicators database table
        pass
    
    def make_recommendation(self):
        # makes recommendation based on all indicators for the stock
        pass