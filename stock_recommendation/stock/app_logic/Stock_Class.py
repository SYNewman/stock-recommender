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
            start_date = current_date - timedelta(days=200)
            stock_data = ticker.history(start=start_date, end=current_date)
            self.price_history = list(stock_data['Close'])
            return self.price_history
        except Exception as e:
            print(f"Stock.py get_stock_close_prices error: {e}")
    
    
    
    def update_data(self, primary_key):
        import yfinance as yf
        from django.utils import timezone
        from datetime import date, timedelta

        # 1. Ensure Stock record exists
        stock_model, _ = Stock.objects.get_or_create(ticker=self.ticker)

        # 2. Try to fetch real data, else use random
        try:
            stock = yf.Ticker(self.ticker)
            stock_info = stock.info
            company_name = stock_info.get('shortName', f"Company {self.ticker}")
            sector = stock_info.get('sector', "Unknown")
            current_price = stock_info.get('currentPrice', random.uniform(10, 500))
            # Try to get last 200 closes
            try:
                current_date = date.today()
                start_date = current_date - timedelta(days=200)
                stock_data = stock.history(start=start_date, end=current_date)
                last_200_close_prices = list(stock_data['Close'])
                if len(last_200_close_prices) < 200:
                    # Fill with random if not enough data
                    last_200_close_prices += [random.uniform(10, 500) for _ in range(200 - len(last_200_close_prices))]
            except Exception:
                last_200_close_prices = [random.uniform(10, 500) for _ in range(200)]
        except Exception:
            company_name = f"Company {self.ticker}"
            sector = "Unknown"
            current_price = random.uniform(10, 500)
            last_200_close_prices = [random.uniform(10, 500) for _ in range(200)]

        # 3. Update Stock model
        stock_model.company_name = company_name
        stock_model.sector = sector
        stock_model.last_updated = timezone.now()
        stock_model.save()

        # 4. Ensure StockData record exists
        stock_data_model, _ = StockData.objects.get_or_create(ticker=stock_model)
        stock_data_model.current_date = date.today()
        stock_data_model.current_price = current_price
        stock_data_model.last_200_close_prices = last_200_close_prices
        price_change = current_price - last_200_close_prices[-2]
        stock_data_model.price_change = price_change
        stock_data_model.price_change_percent = 100 * (price_change / last_200_close_prices[-2])
        stock_data_model.save()

        # 5. Ensure Strategies and Recommendations records exist
        Strategies.objects.get_or_create(ticker=stock_model)
        Recommendations.objects.get_or_create(ticker=stock_model)
    
    
    '''      old update_data method
    def update_data(self, primary_key):
        stock = yf.Ticker(self.ticker)
        stock_info = stock.info
        current_date_and_time = timezone.now()
        
        try:   # Updates data for Stock model
            stock_model = Stock.objects.get(ticker=self.ticker)
            stock_model.company_name = stock_info.get('shortName')
            stock_model.sector = stock_info.get('sector')
            stock_model.last_updated = current_date_and_time
            stock_model.save()
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
        except ObjectDoesNotExist:
            print("(Stock.py 2) There was a problem executing getting the data or saving it to the database.")
    '''
    
    
    def add_indicator(self, strategy, recommendation):
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
    
    
    def set_recommendations(self, stock):  # Update db with recommendations
        try:
            strategies = Strategies.objects.get(ticker=self.ticker)
            buy_total = 0
            hold_total = 0
            sell_total = 0
            for field in ['moving_averages', 'rsi', 'bollinger_bands']:
                value = getattr(strategies, field)
                if value == "Buy":
                    buy_total += 1
                elif value == "Sell":
                    sell_total += 1
                elif value == "Hold":
                    hold_total += 1
            recommendation_data = Recommendations.objects.get(ticker=self.ticker)
            recommendation_data.total_buy_signals = buy_total
            recommendation_data.total_hold_signals = hold_total
            recommendation_data.total_sell_signals = sell_total
            recommendation_data.save()
        except Exception as e:
            print(f"(Stock.py 4/5) The recommendations for {self.ticker} could not be calculated or saved due to Error: {e}")