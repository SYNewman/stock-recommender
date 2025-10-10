import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_recommendation.settings')
django.setup()
#lines 6-9 are necessary to run django scripts outside of the django environment. They were copied from the internet

from stock.models import Stock, StockData, Strategies, Recommendations

list_of_stocks = []
try:
    
    with open("tickers.txt", "r") as stocks: #opens the text file with the list of stocks
        
        for i in stocks:
            try:
                stock = i.strip() #ensures only the ticker is used, not anything else
                list_of_stocks.append(stock)
            except Exception as e:
                print(f"There was a problem loading {i}. The problem was: {e}")
                continue
        
        for i in list_of_stocks:
            stock, created = Stock.objects.get_or_create(ticker=i) #creates a new db record for the stock
            ''' 'created' variable unpacks the tuple so that in the next 3 lines,
            the db record will be created, as it needs to take an object, and without
            this it will pass a whole tuple, which will not work.'''
            
            try: #create related records in the other db tables
                StockData.objects.get_or_create(ticker=stock)
                Strategies.objects.get_or_create(ticker=stock)
                Recommendations.objects.get_or_create(ticker=stock)
            except Exception as e:
                print(f"There was a problem adding {i} to the related tables: {e}")

except Exception as e:
    print(f"(Trading_System.py) List of Stocks could not be loaded. The problem was: {e}")