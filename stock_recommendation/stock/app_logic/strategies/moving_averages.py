from Strategies import Strategy

class Moving_Average_Strategy(Strategy):
    
    def __init__(self, strategy, stats, price):
        super().__init__(strategy, stats)
        self.short_term_moving_average = 0
        self.long_term_moving_average = 0
        self.stats = stats
        self.price = price
        
    def calculate_short_term_moving_average(self):
        total_close_prices = 0
        for i in (close price for each of last 50 trading days): # should be first 50 days of stats
            total_close_prices += i
        self.short_term_moving_average = total_close_prices/50
        
    def calculate_long_term_moving_average(self):
        total_close_prices = 0
        for i in self.stats:
            total_close_prices += i
        self.long_term_moving_average = total_close_prices/200
    
    def generate_signal(self):
        if self.price > self.short_term_moving_average and self.short_term_moving_average > self.long_term_moving_average:
            #buy
        elif self.price < self.short_term_moving_average and self.short_term_moving_average < self.long_term_moving_average:
            #sell
        else:
            #hold
            
    def apply_strategy(self):
        pass