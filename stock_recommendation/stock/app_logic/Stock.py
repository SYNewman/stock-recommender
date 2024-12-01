import yfinance as yf
import models.Stock
import models.StockData
import models.Recommendations

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = None
        self.signals = {}
        self.recommendation = None
        
    # Make this work for the database record which is being updated
    def update_data(self):
        info = self.ticker.info()
        # 'Stock' model
        Stock.ticker = ticker
        Stock.company_name = info['shortName']
        Stock.sector = info['sector']
        # 'StockData' model
        StockData.open_price = info['open']
        StockData.close_price = info['previousClose']
        StockData.high_price = info['dayHigh']
        StockData.low_price = info['dayLow']
        StockData.volume = info['volume']
        #Ignore next 3 lines
        ######Below is alternate code############
        #global Stock_model_data = []
        #global StockData_model_data = []
    
    def add_indicator(self):
        # adds indicator to the indicators database table
        pass
    
    def make_recommendation(self):
        score = 0
        ma = {ma_signal} # put proper var name and real signal from database
        rsi = {rsi_signal}
        bb - {bb_signal}
        
        if ma==buy: # make real logic for checking what the signal is
            score += 1
        elif ma==sell: score -= 1

        if rsi==buy: score += 1
        elif rsi==sell: score -= 1

        if bb==buy: score += 1
        elif bb==sell: score -= 1
            
        if score == 3:
            #very strong buy       # actually make this update the db with the recommendation
        elif score == 2:
            #strong buy
        elif score == 1:
            #buy
        elif score == 0:
            #hold
        elif score == -1:
            #sell
        elif score == -2:
            #strong sell
        elif score == -3:
            #very strong sell
        else: raise Error(f"Recommendation for {self.ticker} could not be calculated")