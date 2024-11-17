class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = None
        self.signals = {}
        self.recommendation = None
        
    def get_data(self):
        pass
    
    