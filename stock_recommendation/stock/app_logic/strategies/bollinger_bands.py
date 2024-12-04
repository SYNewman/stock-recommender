from Strategies import Strategy

class Bollinger_Bands_Strategy(Strategy):
    
    def __init__(self, strategy, price, stats):
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
        for i in (close_price for each of last 20 trading days):
            total += i
        self.mean_close = total/20
                                                                     
    def calculate_deviations(self):
        for i in (close_price for each of last 20 trading days):
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
    
    def calculate_bands(self, mean_close, standard_deviation):
        self.upper_band = self.mean_close + (2 * self.standard_deviation)
        self.lower_band = self.mean_close - (2 * self.standard_deviation)
        
    def generate_signal(self):
        if self.price >= self.upper_band:
            #sell # change to give actual sell signal
        elif self.price <= self.lower_band:
            #buy
        else:
            #hold
            
    def apply_strategy(self):
        pass