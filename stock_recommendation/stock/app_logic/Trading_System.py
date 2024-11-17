class Trading_System:
    def __init__(self, list_of_stocks, list_of_strategies):
        self.list_of_stocks = []
        self.list_of_strategies = []
        self.recommendations = {}
    
    def get_stocks(self, stock: Stock):
        try:
            # put code here to read text file with list of stocks
            # (add .txt file with tickers to the app_logic folder)
            pass
        except: # add here the type of exception
            continue
    
    def add_strategy(self, strategy: Strategy):
        # Adds a new strategy to the list_of_strategies
        pass
    
    def update_data(self):
        #Calls each stock's get_data() method...
        # ...to refresh data
        pass
    
    def run_strategies(self):
        # Iterates over each stock...
        # ...and applies each strategy...
        # ...storing results in recommendations dict.
        pass
    
    def generate_recommendations(self):
        # Processes and aggregates signals...
        # ...from all strategies to make a final...
        # ...recommendation for each stock.
        pass