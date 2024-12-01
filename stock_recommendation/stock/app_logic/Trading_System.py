import Stock
import Strategies

class Trading_System:
    def __init__(self):
        self.list_of_stocks = []
        self.recommendations = {}
    
    def get_stocks(self, stock: Stock):
        try:
            stocks = open("tickers.txt", "r")
            for i in stocks:
                try:
                    i.strip()
                    self.list_of_stocks.append(i)
                except:
                    continue
            stocks.close()
            return self.list_of_stocks
        except:
            raise error("List of Stocks could not be loaded.")
    
    def run_strategies(self):
        # Iterates over each stock and applies each strategy, ...
        # ...storing results in recommendations table in database
        # This method will probably store/run the queue for all tasks
        # This method may need to be split into multiple methods to shorten it
        # work out how this method will work with the queue and with the frontend
        pass