from . import Stock
from . import Strategies
from stock.models import Stock
from stock.models import StockData
from datetime import date, datetime
from collections import deque

class Trading_System:
    
    def __init__(self):
        self.list_of_stocks = []
        self.recommendations = {}
        self.list_of_operations = deque()
    
    def get_stocks(self):
        try:
            with open("tickers.txt", "r") as stocks:
                for i in stocks:
                    try:
                        stock = i.strip()
                        self.list_of_stocks.append(stock)
                        does_stock_exist_in_db = Stock.objects.filter(ticker=stock).exists()
                        if not does_stock_exist_in_db:
                            current_date_and_time = datetime.now()
                            new_stock = Stock(ticker=stock, company_name=None,
                                              sector=None, last_updated=current_date_and_time)
                            new_stock.save()
                    except Exception as exception_type:
                        print(f"There was a problem loading {stock}. The problem was: {exception_type}")
                        continue
            return self.list_of_stocks
        except Exception as exception_type:
            print(f"List of Stocks could not be loaded. The problem was: {exception_type}")
            raise

    def compile_queue(self):
        self.list_of_operations.append(get_stocks())
        for i in self.list_of_stocks:
            try:
                stock_object = Stock(i)
                
                stock_field = Stock.objects.get(ticker=i)
                stock_id = stock_field.stock_id
                
                stock_id_field = StockData.objects.get(stock_id=stock_id)
                close_prices = stock_id_field.last_200_close_prices
                price = stock_id_field.current_price
                
                self.list_of_operations.append(stock_object.update_data(stock_id))
                #runs the moving average strategy
                moving_average_strategy = Moving_Average_Strategy("Moving Averages", close_prices, price)
                self.list_of_operations.append(moving_average_strategy.apply_strategy())
                
                #runs the rsi strategy
                rsi_strategy = RSI_Strategy("RSI", close_prices, price)
                self.list_of_operations.append(rsi_strategy.apply_strategy())
                
                #runs the bollinger bands strategy
                bollinger_band_strategy = Bollinger_Bands_Strategy("Bollinger Bands", close_prices, price)
                self.list_of_operations.append(bollinger_band_strategy.apply_strategy())
                
                self.list_of_operations.append(Stock.make_recommendation(stock_id))
            except Exception as exception_type:
                print(f"The required actions for {i} could not be run due to Error: {exception_type}")
    
    def run_operations(self):
        try:
            while self.list_of_operations:
                operations = self.list_of_operations.popleft()
                operations()
        except Exception as exception_type:
            print(f"The operations could not be executed due to Error: {exception_type}")