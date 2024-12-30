import yfinance as yf
from datetime import datetime, timedelta
import math

class Black_Scholes:
    
    def __init__(self, stock, strike_price, end_date):
        self.call = 0
        self.put = 0
        
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
        # Gets the data
        today = datetime.today()
        start_date = today - timedelta(days=365)
        close_prices = yf.download(self.stock, start_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))['Close']
        
        # Calculates daily returns
        daily_returns = []
        daily_return = 0
        total = 0
        for i in range(1, len(close_prices)):
            daily_return = (close_prices.iloc[i] - close_prices.iloc[i-1]) / close_prices.iloc[i-1]
            total += daily_return
            daily_returns.append(daily_return)
        
        # Calculates variance & sigma
        mean = total/len(daily_returns)
        variance_numerator = 0
        for i in daily_returns:
            variance_numerator += (i-mean)**2
        variance = variance_numerator / (len(daily_returns)-1)
        annual_variance = variance*252
        self.sig = math.sqrt(annual_variance)
    
    def calculate_cumulative_distribution(self, z):
        return (math.erf(z/math.sqrt(2))+1)/2
        
    def calculate_denominator(self):
        self.denominator = self.sig * math.sqrt(self.t)
    
    def calculate_d1(self):
        self.d1 = (math.log(self.s/self.x) + self.t*(self.r+((self.sig**2)/2))) / self.denominator
    
    def calculate_d2(self):
        self.d2 = self.d1 - self.denominator
        
    def calculate_call_price(self):
        d1 = self.calculate_cumulative_distribution(self.d1)
        d2 = self.calculate_cumulative_distribution(self.d2)
        self.call = self.s*d1 - self.x*(math.e**(-1*self.r*self.t))*d2
    
    def calculate_put_price(self):
        d1 = self.calculate_cumulative_distribution(self.d1*-1)
        d2 = self.calculate_cumulative_distribution(self.d2*-1)
        self.put = self.x*(math.e**(-1*self.r*self.t))*d2 - self.s*d1
    
    def calculate_price(self):
        # Calculate the necessary info
        self.calculate_stock_price()
        self.calculate_option_length()
        self.calculate_risk_free_interest_rate()
        self.calculate_volatility()
        # Calculate the option price
        self.get_data()
        self.calculate_denominator()
        self.calculate_d1()
        self.calculate_d2()
        # Calculate final call & put price
        self.calculate_call_price()
        self.calculate_put_price()
        return self.call, self.put