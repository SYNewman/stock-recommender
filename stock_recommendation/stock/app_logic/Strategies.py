class Strategy:
    def __init__(self, strategy, stats):
        self.strategy = ""
        self.stats = {}
        self.signal = ""
        
    def apply_strategy(self, stock: Stock):
        pass


class Moving_Average_Strategy(Strategy):
    def apply_strategy(self, stock):
        # Implement logic for the strategy here
        # Use short_period & long_period parameters...
        # ...to make recommendation
        pass


class RSI_Strategy(Strategy):
    def apply_strategy(self, stock):
        # Implement logic for the strategy here
        pass


class Bollinger_Bands_Strategy(Strategy):
    def apply_strategy(self, stock):
        # Implement logic for the strategy here
        pass