import Stock
import Strategies
from stock.models import Stock
from datetime import date, datetime

class Trading_System:
    
    def __init__(self):
        self.list_of_stocks = []
        self.recommendations = {}
    
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
    
    def run_strategies(self):
        # Iterates over each stock and applies each strategy, ...
        # ...storing results in recommendations table in database
        # This method will probably store/run the queue for all tasks
        # This method may need to be split into multiple methods to shorten it
        # work out how this method will work with the queue and with the frontend
        pass