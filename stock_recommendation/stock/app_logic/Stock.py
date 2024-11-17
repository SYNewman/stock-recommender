class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = None
        self.signals = {}
        self.recommendation = None
        
    def get_data(self):
        # gets data from yfinance
        pass
    
    def update_data(self):
        # updates the database with new data
        pass
    
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