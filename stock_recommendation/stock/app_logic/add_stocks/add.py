import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_recommendation.settings')
django.setup()

from stock.models import Stock, StockData, Strategies, Recommendations

list_of_stocks = []
try:
    
    with open("tickers.txt", "r") as stocks:
        
        for i in stocks:
            try:
                stock = i.strip()
                list_of_stocks.append(stock)
            except Exception as e:
                print(f"There was a problem loading {i}. The problem was: {e}")
                continue
        
        for i in list_of_stocks:
            stock, created = Stock.objects.get_or_create(ticker=i)
            ''' 'created' variable unpacks the tuple so that in the next 3 lines,
            the db record will be created, as it needs to take an object, and without
            this it will pass a whole tuple, which will not work.'''
            
            try:
                StockData.objects.get_or_create(ticker=stock)
                Strategies.objects.get_or_create(ticker=stock)
                Recommendations.objects.get_or_create(ticker=stock)
            except Exception as e:
                print(f"There was a problem adding {i} to the related tables: {e}")

except Exception as e:
    print(f"(Trading_System.py) List of Stocks could not be loaded. The problem was: {e}")