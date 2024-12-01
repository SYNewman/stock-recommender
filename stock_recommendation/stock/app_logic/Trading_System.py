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
    
    def update_data(self):
        data = Stock.get_data()
        return data
    
    def generate_recommendations(self):
        # Processes and aggregates signals...
        # ...from all strategies to make a final...
        # ...recommendation for each stock.
        pass
    
    def run_strategies(self):
        # Iterates over each stock...
        # ...and applies each strategy...
        # ...storing results in recommendations dict.
        pass