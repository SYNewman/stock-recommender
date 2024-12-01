from Strategies import Strategy

class Moving_Average_Strategy(Strategy):
    
    def __init__(self, strategy, stats):
        super().__init__(strategy, stats)
        self.short_term_moving_average = 0
        self.long_term_moving_average = 0
        
    def calculate_short_term_moving_average(self):
        total_close_prices = 0
        for i in (close price for each of last 50 trading days):
            total_close_prices += i
        self.short_term_moving_average = total_close_prices/50
        return self.short_term_moving_average
        
    def calculate_long_term_moving_average(self):
        total_close_prices = 0
        for i in (close price for each of last 200 trading days):
            total_close_prices += i
        self.long_term_moving_average = total_close_prices/200
        return self.long_term_moving_average
    
    def apply_strategy(self, stock): #price var needs to be passed or defined
        if price > self.short_term_moving_average and self.short_term_moving_average > self.long_term_moving_average:
            #buy
        elif price < self.short_term_moving_average and self.short_term_moving_average < self.long_term_moving_average:
            #sell
        else:
            #hold