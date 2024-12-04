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
            stock_model = Stock.objects.get(stock_id=primary_key)
            stock_model.ticker = self.ticker
            stock_model.company_name = stock_info['shortName']
            stock_model.sector = stock_info['sector']
            stock_model.last_updated = current_date_and_time
            stock_model.save()
        except ObjectDoesNotExist:
            print("There was a problem executing getting the data or saving it to the database.")
        
        # Updates data for StockData model
        try:
            stock_data_model = StockData.objects.get(stock_id=primary_key)
            stock_data_model.current_date = date.today()
            stock_data_model.current_price = stock_info['currentPrice']
            stock_data_model.last_200_close_prices = get_stock_close_prices()
            stock_data_model.save()
        except ObjectDoesNotExist:
            print("There was a problem executing getting the data or saving it to the database.")
    
    
    def add_indicator(self, strategy, primary_key, recommendation):
        try:
            stock_record = Recommendations.objects.get(stock_id=primary_key)
            if strategy == "moving_averages":
                stock_record.moving_averages_signal = recommendation
            elif strategy == "rsi":
                stock_record.rsi_signal = recommendation
            elif strategy == "bollinger_bands":
                stock_record.bollinger_bands_signal = recommendation
            stock_record.save()
        except Exception as exception_type:
            print(f"The {strategy} indicator for {self.ticker} could not be added to the database due to Error: {exception_type}")
    
    
    def make_recommendation(self, primary_key):
        recommendation = ""
        score = 0
        
        try:
            all_signals = Recommendations.objects.get(stock_id=primary_key)
            moving_average_signal = all_signals.moving_average_signal
            rsi_signal = all_signals.rsi_signal
            bollinger_bands_signal = all_signals.bollinger_bands_signal
        except Recommendations.DoesNotExist:
            print(f"The trading signals for {self.ticker} could not be loaded to due Error: {exception_type}")
            
        try:
            if moving_average_signal == "Buy": score += 1
            elif moving_average_signal == "Sell": score -= 1

            if rsi_signal == "Buy": score += 1
            elif rsi_signal == "Sell": score -= 1

            if bollinger_bands_signal == "Buy": score += 1
            elif bollinger_bands_signal == "Sell": score -= 1
                
            if score == 3: recommendation = "Very Strong Buy"
            elif score == 2: recommendation = "Strong Buy"
            elif score == 1: recommendation = "Buy"
            elif score == 0: recommendation = "Hold"
            elif score == -1: recommendation = "Sell"
            elif score == -2: recommendation = "Strong Sell"
            elif score == -3: recommendation = "Very Strong Sell"
        except Exception as exception_type:
            print(f"The recommendation for {self.ticker} could not be calculated due to Error: {exception_type}")
        
        try:
            update_db = Recommendations.objects.get(stock_id=primary_key)
            update_db.overall_recommendation = recommendation
            update_db.save()
        except Exception as exception_type:
            print(f"The final recommendation for {self.ticker} could not be saved to the database due to Error: {exception_type}")