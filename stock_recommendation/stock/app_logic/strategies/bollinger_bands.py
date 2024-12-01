from Strategies import Strategy

class Bollinger_Bands_Strategy(Strategy):
    
    # maybe add queue here to run all methods to generate recommendation
    # however, consider how this will effect/work with planned queue...
    # ... in trading_system for all operations to generate recommendations
    
    def __init__(self, strategy, stats):
        super().__init__(strategy, stats)
        self.mean_close = 0
        self.standard_deviation = 0
        self.upper_band = 0
        self.lower_band = 0
    
    def calculate_mean_close(self):
        total = 0
        #for i in (close_price for each of last 20 trading days): # make the for loop work
            #total += i
        self.mean_close = total/20
        return self.mean_close
                                                                     
    def calculate_deviations(self, mean_close):
        all_deviations = []
        for i in (close_price for each of last 20 trading days):
            deviation = i - self.mean_close
            squared_deviation = deviation*deviation
            all_deviations.append(squared_deviation)
        return all_deviations
    
    def calculate_variance(self, deviations):
        total_variance = 0
        for i in deviations:
            total_variance += i
        variance = total_variance/20
        return variance
        
    def calculate_standard_deviation(self, variance):
        self.standard_deviation = variance ** 0.5
        return self.standard_deviation
    
    def calculate_bands(self, mean_close, standard_deviation):
        self.upper_band = mean_close + (2 * standard_deviation)
        self.lower_band = mean_close - (2 * standard_deviation)
        
    def apply_strategy(self, stock):
        #if stock_price >= self.upper_band: #change 'stock_price' to the actual stock price
            #sell # change to give actual sell signal
        #elif stock_price <= self.lower_band:
            #buy
        #else:
            #hold
        pass