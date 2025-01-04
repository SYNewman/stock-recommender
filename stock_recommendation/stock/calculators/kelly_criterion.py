class Kelly_Criterion:
    
    '''
    This class uses the Kelly Criterion to calculate how much of a trader's capital should
    be put into a single trade (as a percentage). Search online to view the formula for the
    Kelly Criterion, or to understand how it works.
        
    Variables named with only a letter (self.w, self.r & self.k) refer to the
    one-letter value with which that variable is presented in the mathematical
    representation of the formula. For example, self.w refers to the historical
    win percentage of a trading system, which is represented as 'W' or 'w' in
    mathematical representations.
    '''
    
    def __init__(self, trade_amount, trade_wins, average_win, average_loss):
        self.trade_amount = trade_amount
        self.trade_wins = trade_wins
        self.average_win = average_win
        self.average_loss = average_loss
        self.w = 0
        self.r = 0
        self.k = 0
        
    def calculate_win_percent(self):
        if self.trade_amount == 0: # Handle edge cases
            self.trade_amount == 1
        self.w = self.trade_wins / self.trade_amount
        
    def calculate_win_loss_ratio(self):
        if self.average_loss == 0: # Handle edge cases
            self.average_loss == 1
        self.r = self.average_win / self.average_loss
        
    def calculate_kelly_percent(self):
        w = self.w
        r = self.r
        self.k = w - ((1-w)/r)
        self.k = round(self.k, 2)