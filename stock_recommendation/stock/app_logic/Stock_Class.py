import random
import yfinance as yf
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime, timedelta
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
            start_date = current_date - timedelta(days=200) #gets data for the last 200 days
            stock_data = ticker.history(start=start_date, end=current_date)
            self.price_history = list(stock_data['Close'])
            return self.price_history
        except Exception as e:
            print(f"Stock.py get_stock_close_prices error: {e}")
    
    
    
    def update_data(self, primary_key):
        #ensure Stock record exists
        stock_model, _ = Stock.objects.get_or_create(ticker=self.ticker)

        #try to fetch real data, otherwise use random data
        company_name = f"{self.ticker}"
        sector = "Unknown"
        current_price = random.uniform(10, 200) #gives a random price between 10 and 200
        last_200_close_prices = [random.uniform(10, 200) for _ in range(200)] #does the same for last 200 close prices

        try: #to get the real stock data
            stock = yf.Ticker(self.ticker)
            stock_info = stock.info
            company_name = stock_info.get('shortName', company_name)
            sector = stock_info.get('sector', sector)
            fetched_price = stock_info.get('currentPrice')
            if fetched_price is not None and isinstance(fetched_price, (int, float)): #checks that the price is a number
                current_price = fetched_price

            try: #try to get last 200 close prices
                current_date = date.today()
                start_date = current_date - timedelta(days=200)
                stock_data = stock.history(start=start_date, end=current_date)
                closes = list(stock_data['Close'])
                if closes and all(isinstance(x, (int, float)) for x in closes):
                    #fill with random data if there is not enough data
                    if len(closes) < 200:
                        closes += [random.uniform(10, 500) for _ in range(200 - len(closes))]
                    last_200_close_prices = closes[:200]
            except Exception:
                pass  #uses random data already set above
        except Exception:
            pass  #uses random data already set above

        #update the db with the new data
        stock_model.company_name = company_name
        stock_model.sector = sector
        stock_model.last_updated = timezone.now()
        stock_model.save()
       
        #stock_data model
        stock_data_model, _ = StockData.objects.get_or_create(ticker=stock_model) #ensure record exists
        stock_data_model.current_date = date.today()
        stock_data_model.current_price = current_price
        stock_data_model.last_200_close_prices = last_200_close_prices
        price_change = current_price - last_200_close_prices[-2]
        stock_data_model.price_change = price_change
        stock_data_model.price_change_percent = 100 * (price_change / last_200_close_prices[-2])
        stock_data_model.save()

        #ensure Strategies and Recommendations records exist
        Strategies.objects.get_or_create(ticker=stock_model)
        Recommendations.objects.get_or_create(ticker=stock_model)
    
    
    def add_indicator(self, strategy, recommendation): # Update db with each strategy's recommendation
        try:
            stock_record = Strategies.objects.get(ticker=self.ticker)
            if strategy == "moving averages":
                stock_record.moving_averages = recommendation
            elif strategy == "rsi":
                stock_record.rsi = recommendation
            elif strategy == "bollinger bands":
                stock_record.bollinger_bands = recommendation
            else:
                print("There seems to be an error adding an indicator")
            stock_record.save()
        except Exception as e:
            print(f"(Stock.py 3) The {strategy} indicator for {self.ticker} could not be added to the database due to Error: {e}")
    
    
    def set_recommendations(self, stock):  # Update db with total recommendations
        try:
            strategies = Strategies.objects.get(ticker=self.ticker)
            buy_total = 0
            hold_total = 0
            sell_total = 0
            # calculate totals
            for i in ['moving_averages', 'rsi', 'bollinger_bands']:
                value = getattr(strategies, i)
                if value == "Buy":
                    buy_total += 1
                elif value == "Sell":
                    sell_total += 1
                elif value == "Hold":
                    hold_total += 1
            # save totals in the db
            recommendation_data = Recommendations.objects.get(ticker=self.ticker)
            recommendation_data.total_buy_signals = buy_total
            recommendation_data.total_hold_signals = hold_total
            recommendation_data.total_sell_signals = sell_total
            recommendation_data.save()
        except Exception as e:
            print(f"(Stock.py 4/5) The recommendations for {self.ticker} could not be calculated or saved due to Error: {e}")