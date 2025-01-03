from . import Stock
from . import Strategies
from stock.models import Stock
from stock.models import StockData
from stock.models import Recommendations
from datetime import date, datetime
from collections import deque
from .strategies.moving_averages import Moving_Average_Strategy
from .strategies.rsi import RSI_Strategy
from .strategies.bollinger_bands import Bollinger_Bands_Strategy

class Trading_System:
    
    def __init__(self):
        self.list_of_stocks = []
        self.recommendations = {}
        self.list_of_operations = deque()
    
    def get_stocks(self):
        try:
            with open("stock/app_logic/tickers_short.txt", "r") as stocks:
                for i in stocks:
                    try:
                        stock = i.strip()
                        self.list_of_stocks.append(stock)
                        does_stock_exist_in_db = Stock.objects.filter(ticker=stock).exists()
                        stock_db = Stock.objects.filter(ticker=stock).first()
                        stock_id = stock_db.stock_id
                        does_StockData_exist = StockData.objects.filter(stock_id=stock_id).exists()
                        does_Recommendations_exist = Recommendations.objects.filter(stock_id=stock_id).exists()
                        if does_stock_exist_in_db==False or does_StockData_exist==False or does_Recommendations_exist==False:
                            current_date_and_time = datetime.now()
                            today = date.today()
                            does_this_stock_exist = Stock.objects.filter(ticker=stock).exists()
                            if does_this_stock_exist == True:
                                Stock.objects.filter(ticker=stock).delete()
                            Stock.objects.create(
                                ticker=stock,
                                company_name=None,
                                sector=None,
                                last_updated=current_date_and_time)
                            stock_db = Stock.objects.filter(ticker=stock).first()
                            stock_id = stock_db.stock_id
                            StockData.objects.create(
                                stock_id=stock_id,
                                current_date=today,
                                current_price=None,
                                last_200_close_prices=None,
                            )
                            Recommendations.objects.create(
                                stock_id=stock_id,
                                moving_average_signal=None,
                                rsi_signal=None,
                                bollinger_bands_signal=None,
                                overall_recommendation=None,
                            )
                    except Exception as exception_type:
                        print(f"There was a problem loading {stock}. The problem was: {exception_type}")
                        continue
            return self.list_of_stocks
        except Exception as exception_type:
            print(f"(Trading_System.py) List of Stocks could not be loaded. The problem was: {exception_type}")
            raise

    def compile_queue(self):
        self.get_stocks()
        for i in self.list_of_stocks:
            try:
                stock_object = Stock(i)
                stock_field = Stock.objects.get(ticker=i)
                stock_id = stock_field.stock_id
            except: print("Error 1")
            try:
                stock_id_field = Stock.objects.get(stock_id=stock_id)
                close_prices = stock_id_field.last_200_close_prices
                price = stock_id_field.current_price
            except exception as e:
                print(f"This doesn't work: {e}")
            try:
                self.list_of_operations.append(lambda:stock_object.update_data(stock_id))
                
                #runs the moving average strategy
                moving_average_strategy = Moving_Average_Strategy("Moving Averages", close_prices, price)
                self.list_of_operations.append(lambda:moving_average_strategy.apply_strategy())
                
                #runs the rsi strategy
                rsi_strategy = RSI_Strategy("RSI", close_prices, price)
                self.list_of_operations.append(lambda:rsi_strategy.apply_strategy())
                
                #runs the bollinger bands strategy
                bollinger_band_strategy = Bollinger_Bands_Strategy("Bollinger Bands", close_prices, price)
                self.list_of_operations.append(lambda:bollinger_band_strategy.apply_strategy())
                
                self.list_of_operations.append(lambda:Stock.make_recommendation(stock_id))
            except Exception as exception_type:
                print(f"(Trading_System.py) The required actions for {i} could not be run due to Error: {exception_type}")
    
    def run_operations(self):
        try:
            while self.list_of_operations:
                operations = self.list_of_operations.popleft()
                operations()
        except Exception as exception_type:
            print(f"(Trading_System.py) The operations could not be executed due to Error: {exception_type}")