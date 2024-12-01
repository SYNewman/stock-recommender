from Strategies import Strategy

class RSI_Strategy(Strategy):
    
    def __init__(self, strategy, stats):
        super().__init__(strategy, stats)
        self.time_period = 14
    
    def calculate_daily_price_change(self):
        all_changes = []
        for i in range(len(self.stats-1)):
            price_change = self.stats[i]['price'] - self.stats[i+1]['price']
            all_changes.append(price_change)
        return all_changes
    
    def separate_gains_and_losses(self, changes):
        gains = []
        losses = []
        for i in changes:
            if i > 0:
                gains.append(i)
                losses.append(0)
            elif i < 0:
                gains.append(0)
                losses.append(i*-1)
            else:
                gains.append(0)
                losses.append(0)
        return gains, losses
    
    def calculate_average_gain(self, gains): # This and next method - maybe put into one smaller method
        total_gain = 0
        for i in gains:
            total_gain += i
        average_gain = total_gain / self.time_period
        return average_gain
    
    def calculate_average_loss(self, losses):
        total_loss = 0
        for i in losses:
            total_loss += i
        average_loss = total_loss / self.time_period
        return average_loss
    
    def calculate_second_average_gain(self, average_gain): # To smooth out the values
        current_gain = price - self.stats[i['price']]
        if current_gain < 0:
            current_gain = 0
        previous_average_gain = average_gain * (self.time_period - 1)
        second_average_gain = (previous_average_gain + current_gain) / self.time_period
        return second_average_gain
        
    def calculate_second_average_loss(self, average_loss): # To smooth out the values
        current_loss = price - self.stats[i['price']] # put real price (at runtime) here
        if current_loss < 0:
            current_loss = 0
        previous_average_loss = average_loss * (self.time_period - 1)
        second_average_loss = (previous_average_loss + current_loss) / self.time_period
        return second_average_loss
    
    def calculate_relative_strength(self, second_average_gain, second_average_loss):
        if second_average_loss == 0:
            return float('inf')
        rs = second_average_gain / second_average_loss
        return rs
    
    def calculate_rsi_value(self, rs):
        rsi = 100 - (100 / (rs+1))
        return rsi
    
    def apply_strategy(self, stock, rsi):
        if rsi < 30:
            #buy
        elif rsi > 70:
            #sell
        else:
            #hold