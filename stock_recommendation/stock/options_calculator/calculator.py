import yfinance as yf

class Black_Scholes:
    
    def __init__(self, option_type, stock, strike_price, end_date):
        self.type = option_type
        
        self.stock = stock
        self.s = None
        
        self.end_date = end_date
        self.t = None
        
        self.r = None
        
        self.x = strike_price
        self.sig = None
        
        self.N = None
        
        self.denominator = 0
        self.d1 = 0
        self.d2 = 0
        self.price = 0
        
    def calculate_stock_price(self):
        stock = yf.ticker(self.stock)
        self.s = stock.fast_info['lastPrice']
    
    def calculate_option_length(self):
        pass
    
    def calculate_risk_free_interest_rate(self):
        pass
    
    def calculate_volatility(self):
        pass
    
    def calculate_cumulative_distribution(self):
        pass
    
    def get_data(self):
        calculate_stock_price(self)
        calculate_option_length(self)
        calculate_risk_free_interest_rate(self)
        calculate_volatility(self)
        calculate_cumulative_distribution(self)
        
    def calculate_denominator(self):
        pass
    
    def calculate_d1(self):
        pass
    
    def calculate_d2(self):
        self.d2 = self.d1 - self.denominator
        
    def calculate_call_price(self):
        pass
    
    def calculate_put_price(self):
        pass
    
    def calculate_price(self):
        get_data(self)
        calculate_denominator(self)
        calculate_d1(self)
        calculate_d2(self)
        if self.type == "call":
            calculate_call_price(self)
        elif self.type == "put":
            calculate_put_price(self)
        else:
            self.price = "The options price could not be calculated"
        return self.price