import yfinance as yf
import datetime
import math

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
        stock = yf.Ticker(self.stock)
        self.s = stock.fast_info['lastPrice']
    
    def calculate_option_length(self):
        today = datetime.today()
        end_date = datetime(self.end_date)
        length = today - end_date
        difference = length.days
        self.t = difference / 365
    
    def calculate_risk_free_interest_rate(self):
        rate_ticker = yf.Ticker("^TNX")
        interest_rate = rate_ticker.fast_info['lastPrice']
        self.r = interest_rate / 100
    
    def calculate_volatility(self):
        pass
    
    def calculate_cumulative_distribution(self, z):
        return (math.erf(z/math.sqrt(2))+1)/2
        
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
        # Calculate the necessary info
        calculate_stock_price(self)
        calculate_option_length(self)
        calculate_risk_free_interest_rate(self)
        calculate_volatility(self)
        # Calculate the option price
        get_data(self)
        calculate_denominator(self)
        calculate_d1(self)
        calculate_d2(self)
        # Set option price
        if self.type == "call": calculate_call_price(self)
        elif self.type == "put": calculate_put_price(self)
        return self.price