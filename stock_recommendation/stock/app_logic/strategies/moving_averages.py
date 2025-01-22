from stock.models import Stock
from stock.app_logic.Strategies import Strategy
from stock.app_logic.Stock_Class import Stock_Class

class Moving_Average_Strategy(Strategy):
    
    def __init__(self, ticker):
        super().__init__(ticker)
        self.short_term_moving_average = 0
        self.long_term_moving_average = 0
        
    def calculate_short_term_moving_average(self):
        total_close_prices = 0
        for i in self.stats[151:200]:
            total_close_prices += i
        self.short_term_moving_average = total_close_prices/50
        
    def calculate_long_term_moving_average(self):
        total_close_prices = 0
        for i in self.stats:
            total_close_prices += i
        self.long_term_moving_average = total_close_prices/200
    
    def generate_signal(self):
        stock_field = Stock.objects.get(ticker=self.ticker)
        ticker = stock_field.ticker
        stock = Stock_Class(ticker)
        
        if self.price > self.short_term_moving_average and self.short_term_moving_average > self.long_term_moving_average:
            stock.add_indicator("moving averages", "Buy")
        elif self.price < self.short_term_moving_average and self.short_term_moving_average < self.long_term_moving_average:
            stock.add_indicator("moving averages", "Sell")
        else:
            stock.add_indicator("moving averages", "Hold")
            
    def apply_strategy(self):
        self.calculate_short_term_moving_average()
        self.calculate_long_term_moving_average()
        self.generate_signal()