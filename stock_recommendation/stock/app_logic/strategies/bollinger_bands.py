from Strategies import Strategy
import models.Stock

class Bollinger_Bands_Strategy(Strategy):
    
    def __init__(self, strategy, stats, price):
        super().__init__(strategy, stats)
        self.price = price
        self.stats = stats
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
        stock_field = Stock.objects.get(ticker=i)
        stock_id = stock_field.stock_id
        
        if self.price >= self.upper_band:
            Stock.add_indicator("bollinger bands", stock_id, "Sell")
        elif self.price <= self.lower_band:
            Stock.add_indicator("bollinger bands", stock_id, "Buy")
        else:
            Stock.add_indicator("bollinger bands", stock_id, "Hold")
            
    def apply_strategy(self):
        calculate_mean_close(self)
        calculate_deviations(self)
        calculate_variance(self)
        calculate_standard_deviation(self)
        calculate_bands(self)
        generate_signal(self)