from stock.models import Stock
from stock.app_logic.Strategies import Strategy
from stock.app_logic.Stock_Class import Stock_Class

class Bollinger_Bands_Strategy(Strategy):
    
    def __init__(self, ticker):
        super().__init__(ticker)
        self.mean_close = 0
        self.standard_deviation = 0
        self.upper_band = 0
        self.lower_band = 0
        self.deviations = []
        self.variance = 0
        self.standard_deviation = 0
    
    def calculate_mean_close(self):
        total = 0
        for i in self.stats[181:200]:
            total += i
        self.mean_close = total/20
                                                                     
    def calculate_deviations(self):
        for i in self.stats[181:200]:
            deviation = i - self.mean_close
            squared_deviation = deviation*deviation
            self.deviations.append(squared_deviation)
    
    def calculate_variance(self):
        total_variance = 0
        for i in self.deviations:
            total_variance += i
        self.variance = total_variance/20
        
    def calculate_standard_deviation(self):
        self.standard_deviation = self.variance ** 0.5
    
    def calculate_bands(self):
        self.upper_band = self.mean_close + (2 * self.standard_deviation)
        self.lower_band = self.mean_close - (2 * self.standard_deviation)
        
    def generate_signal(self):
        stock_field = Stock.objects.get(ticker=self.ticker)
        ticker = stock_field.ticker
        stock = Stock_Class(ticker)
        
        if self.price >= self.upper_band:
            stock.add_indicator("bollinger bands", "Sell")
        elif self.price <= self.lower_band:
            stock.add_indicator("bollinger bands", "Buy")
        else:
            stock.add_indicator("bollinger bands", "Hold")
            
    def apply_strategy(self):
        self.calculate_mean_close()
        self.calculate_deviations()
        self.calculate_variance()
        self.calculate_standard_deviation()
        self.calculate_bands()
        self.generate_signal()