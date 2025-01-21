from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime, timedelta
import yfinance as yf
from stock.models import Stock, StockData, Strategies, Recommendations
from django.utils import timezone


class Stock_Class:
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = []
        self.signals = {}
        self.recommendation = None
        
    
    def get_stock_close_prices(self):
        try:
            current_date = date.today()
            ticker = yf.Ticker(self.ticker)
            start_date = current_date - timedelta(days=200)
            stock_data = ticker.history(start=start_date, end=current_date)
            self.price_history = list(stock_data['Close'])
            print("Everything seems fine with getting the stocks close prices")
            return self.price_history
        except Exception as e:
            print(f"Stock.py get_stock_close_prices error: {e}")
    
    
    def update_data(self, primary_key):
        stock = yf.Ticker(self.ticker)
        stock_info = stock.info
        current_date_and_time = timezone.now()
        print("Getting the preliminary info seems to be ok")
        
        try:   # Updates data for Stock model
            stock_model = Stock.objects.get(ticker=self.ticker)
            stock_model.company_name = stock_info.get('shortName')
            stock_model.sector = stock_info.get('sector')
            stock_model.last_updated = current_date_and_time
            stock_model.save()
            print("Updating the Stock model seems to have been successful")
        except ObjectDoesNotExist:
            print("(Stock.py 1) There was a problem executing getting the data or saving it to the database.")
        
        try:   # Updates data for StockData model
            stock_data_model = StockData.objects.get(ticker=self.ticker)
            stock_data_model.current_date = date.today()
            stock_data_model.current_price = stock_info['currentPrice']
            stock_data_model.last_200_close_prices = self.get_stock_close_prices()
            price_change = stock_data_model.current_price - stock_data_model.last_200_close_prices[-2]
            stock_data_model.price_change = price_change
            stock_data_model.price_change_percent = 100*(price_change/stock_data_model.last_200_close_prices[-2])
            stock_data_model.save()
            print("Updating the Stock Data model seems to have been successful")
        except ObjectDoesNotExist:
            print("(Stock.py 2) There was a problem executing getting the data or saving it to the database.")
    
    
    def add_indicator(self, strategy, recommendation):
        try:
            stock_record = Strategies.objects.get(ticker=self.ticker)
            if strategy == "moving averages":
                stock_record.moving_averages_signal = recommendation
            elif strategy == "rsi":
                stock_record.rsi_signal = recommendation
            elif strategy == "bollinger bands":
                stock_record.bollinger_bands_signal = recommendation
            else:
                print("There seems to be an error adding an indicator")
            stock_record.save()
            print("Adding an indicator seems to have been successful")
        except Exception as e:
            print(f"(Stock.py 3) The {strategy} indicator for {self.ticker} could not be added to the database due to Error: {e}")
    
    
    def set_recommendations(self, stock):  # Update db with recommendations
        recommendation_data = Recommendations.objects.get(ticker=self.ticker)
        print("Getting the recommendation data seems to have been successful")
            
        try:  # Count amount of each recommendation
            buy_total = 0
            hold_total = 0
            sell_total = 0
            for i in Recommendations._meta.fields:
                if getattr(recommendation_data, i.name) == "Buy":
                    buy_total += 1
                elif getattr(recommendation_data, i.name) == "Sell":
                    sell_total += 1
                else:
                    hold_total += 1
            print(f"Counting the total recommendation totals for {stock} seems to have worked")
        except Exception as e:
            print(f"(Stock.py 4) The recommendations for {self.ticker} could not be calculated due to Error: {e}")
            
        try:  # Update db with new totals
            recommendation_data.total_buy_signals = buy_total
            recommendation_data.hold_buy_signals = hold_total
            recommendation_data.sell_buy_signals = sell_total
            recommendation_data.save()
            print(f"Updating the db with new recommendation totals for {stock} seems to have worked")
        except Exception as e:
            print(f"(Stock.py 5) The recommendations for {self.ticker} could not be saved to the database due to Error: {e}")