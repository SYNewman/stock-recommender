from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime
import yfinance as yf

import models.Stock
import models.StockData
import models.Recommendations


class Stock:
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = []
        self.signals = {}
        self.recommendation = None
        
    
    def get_stock_close_prices(self):
        current_date = date.today()
        ticker = yf.Ticker(self.ticker)
        start_date = current_date - timedelta(days=200)
        stock_data = ticker.history(start=start_date, end=current_date)
        self.price_history = list(stock_data['Close'])
        return self.price_history
    
    
    def update_data(self, primary_key):
        stock = yf.Ticker(self.ticker)
        stock_info = stock.info
        current_date_and_time = datetime.now()
        
        # Updates data for Stock model
        try:
            stock_model = Stock.objects.get(id=primary_key)
            stock_model.ticker = self.ticker
            stock_model.company_name = stock_info['shortName']
            stock_model.sector = stock_info['sector']
            stock_model.last_updated = current_date_and_time
            stock_model.save()
        except ObjectDoesNotExist:
            print("There was a problem executing getting the data or saving it to the database.")
        
        # Updates data for StockData model
        try:
            stock_data_model = StockData.objects.get(id=primary_key)
            stock_data_model.current_date = date.today()
            stock_data_model.current_price = stock_info['currentPrice']
            stock_data_model.last_200_close_prices = get_stock_close_prices()
            stock_data_model.save()
        except ObjectDoesNotExist:
            print("There was a problem executing getting the data or saving it to the database.")
    
    
    def add_indicator(self):
        # adds indicator to the indicators database table
        pass
    
    
    def make_recommendation(self):
        score = 0
        ma = {ma_signal} # put proper var name and real signal from database
        rsi = {rsi_signal}
        bb - {bb_signal}
        
        if ma==buy: # make real logic for checking what the signal is
            score += 1
        elif ma==sell: score -= 1

        if rsi==buy: score += 1
        elif rsi==sell: score -= 1

        if bb==buy: score += 1
        elif bb==sell: score -= 1
            
        if score == 3:
            #very strong buy       # actually make this update the db with the recommendation
        elif score == 2:
            #strong buy
        elif score == 1:
            #buy
        elif score == 0:
            #hold
        elif score == -1:
            #sell
        elif score == -2:
            #strong sell
        elif score == -3:
            #very strong sell
        else: raise Error(f"Recommendation for {self.ticker} could not be calculated")