import yfinance as yf
from datetime import date, datetime, timedelta
import math

class Black_Scholes:
    
    def __init__(self, stock, strike_price, end_date):
        '''
        This calculator uses the Black-Scholes model for calculating options prices
        See the 'Key Algorithms' section of the 'Design' part of the project documentation
        to view the formula for this model, or to understand how it works
        
        Variables named with only a letter (e.g. self.t or self.s) refer to the
        one-letter value with which that variable is presented in the mathematical
        representation of the formula (for example, self.t refers to the time-to-expiration,
        which is represented as 'T' or 't' in mathematical representations.)
        '''
        
        self.call = 0
        self.put = 0
        self.error = 0
        
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
        try:
            stock = yf.Ticker(self.stock)
            self.s = stock.fast_info['lastPrice']
        except Exception as e:
            print(f"Options Pricing Calculator Error 1: {e}")
            self.error = 1
    
    def calculate_option_length(self):
        try:
            today = date.today()
            length = self.end_date - today
            difference = length.days
            self.t = difference / 365
        except Exception as e:
            print(f"Options Pricing Calculator Error 2: {e}")
            self.error = 1
    
    def calculate_risk_free_interest_rate(self):
        try:
            rate_ticker = yf.Ticker("^TNX") # To calculate the options price, the risk-free interest rate is needed
            interest_rate = rate_ticker.fast_info['lastPrice']
            self.r = interest_rate / 100
        except Exception as e:
            print(f"Options Pricing Calculator Error 3: {e}")
            self.error = 1
    
    def calculate_volatility(self):
        try: # Gets the data
            today = datetime.today()
            start_date = today - timedelta(days=365)
            close_prices = yf.download(self.stock, start_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))['Close']
        except Exception as e:
            print(f"Options Pricing Calculator Error 4: {e}")
            self.error = 1
        
        try: # Calculates daily returns
            daily_returns = []
            daily_return = 0
            total = 0
            for i in range(1, len(close_prices)):
                daily_return = (close_prices.iloc[i] - close_prices.iloc[i-1]) / close_prices.iloc[i-1]
                total += daily_return
                daily_returns.append(daily_return)
        except Exception as e:
            print(f"Options Pricing Calculator Error 5: {e}")
            self.error = 1
        
        try: # Calculates variance & sigma
            mean = total/len(daily_returns)
            variance_numerator = 0
            for i in daily_returns:
                variance_numerator += (i-mean)**2
            variance = variance_numerator / (len(daily_returns)-1)
            annual_variance = variance*252
            self.sig = math.sqrt(float(annual_variance.iloc[0]))
            # The syntax above is to account for future type errors
        except Exception as e:
            print(f"Options Pricing Calculator Error 6: {e}")
            self.error = 1
    
    def calculate_cumulative_distribution(self, z):
        try:
            return (math.erf(z/math.sqrt(2))+1)/2
        except Exception as e:
            print(f"Options Pricing Calculator Error 7: {e}")
            self.error = 1
        
    def calculate_d1_and_d2(self):
        try:
            self.denominator = self.sig * math.sqrt(self.t)
            self.d1 = (math.log(self.s/self.x) + self.t*(self.r+((self.sig**2)/2))) / self.denominator
            self.d2 = self.d1 - self.denominator
        except Exception as e:
            print(f"Options Pricing Calculator Error 8: {e}")
            self.error = 1
        
    def calculate_call_price(self):
        try:
            d1 = self.calculate_cumulative_distribution(self.d1)
            d2 = self.calculate_cumulative_distribution(self.d2)
            self.call = self.s*d1 - self.x*(math.e**(-1*self.r*self.t))*d2
        except Exception as e:
            print(f"Options Pricing Calculator Error 9: {e}")
            self.error = 1
    
    def calculate_put_price(self):
        try:
            d1 = self.calculate_cumulative_distribution(self.d1*-1)
            d2 = self.calculate_cumulative_distribution(self.d2*-1)
            self.put = self.x*(math.e**(-1*self.r*self.t))*d2 - self.s*d1
        except Exception as e:
            print(f"Options Pricing Calculator Error 10: {e}")
            self.error = 1
    
    def calculate_price(self):
        try: # Calculate the necessary info
            self.calculate_stock_price()
            self.calculate_option_length()
            self.calculate_risk_free_interest_rate()
            self.calculate_volatility()
        except Exception as e:
            print(f"Options Pricing Calculator Error 11: {e}")
            self.error = 1
        
        try: # Calculate the call & put price
            self.calculate_d1_and_d2()
            self.calculate_call_price()
            self.calculate_put_price()
        except Exception as e:
            print(f"Options Pricing Calculator Error 12: {e}")
            self.error = 1
            
        try: # Round option prices to 2dp
            self.call = round(self.call, 2)
            self.put = round(self.put, 2)
        except Exception as e:
            print(f"Options Pricing Calculator Error 13: {e}")
            self.error = 1
        
        if self.error == 1: # Accounts for errors
            self.call = "There was a problem calculating the call price."
            self.put = "There was a problem calculating the put price."
        
        return self.call, self.put