from django.shortcuts import render
from .models import Stock
from .models import StockData
from .models import Recommendations
from .app_logic import Trading_System
import traceback
from datetime import datetime
from stock.options_calculator.calculator import Black_Scholes

# Create your views here.
def home_page(request):
    return render(request, "home.html")

def sign_up_page(request):
    return render (request, "sign_up.html")

def log_in_page(request):
    return render (request, "log_in.html")

def recommendations_page(request):
    try:
        trading_system = Trading_System.Trading_System()
        trading_system.compile_queue()
        trading_system.run_operations()
    except Exception as exception_type:
        print(f"(views.py 1) The Stocks could not be updated due to Error: {exception_type}")
    
    all_stocks = Stock.objects.all()
    all_recommendations = Recommendations.objects.all()
    
    very_strong_buy = []
    strong_buy = []
    buy = []
    hold = []
    sell = []
    strong_sell = []
    very_strong_sell = []
    error = []
    
    for i in all_stocks:
        try:
            stock_data = Stock.objects.filter(stock_id=i.stock_id).first()
            stock = stock_data.ticker
        except Exception as exception_type:
            print(f"(views.py 2) The stock {i} could not be loaded due to Error: {exception_type}")
        try:
            #recommendation_data = Stock.objects.filter(stock_id=i.stock_id).first()
            #recommendation_data = Recommendations.objects.filter(stock_id=i.stock_id).first()
            #recommendation_data = Stock.objects.get(stock_id=i.stock_id)
            recommendation_data = Recommendations.objects.get(stock_id=i.stock_id)
        except Exception as exception_type:
            print(f"(views.py 3) The recommendation for {i} could not be accessed due to Error: {exception_type}")
        try:
            recommendation = recommendation_data.overall_recommendation
        except Exception as exception_type:
            recommendation = None
            print(f"(views.py 4) The recommendation for {i} could not be accessed due to Error: {exception_type}")
            traceback.print_exc()
            
        if recommendation == "Very Strong Buy": very_strong_buy.append(stock)
        elif recommendation == "Strong Buy": strong_buy.append(stock)
        elif recommendation == "Buy": buy.append(stock)
        elif recommendation == "Hold": hold.append(stock)
        elif recommendation == "Sell": sell.append(stock)
        elif recommendation == "Strong Sell": strong_sell.append(stock)
        elif recommendation == "Very Strong Sell": very_strong_sell.append(stock)
        elif recommendation == None: error.append(stock)
        
    context = {
        "very_strong_buy": very_strong_buy,
        "strong_buy": strong_buy,
        "buy": buy,
        "sell": sell,
        "strong_sell": strong_sell,
        "very_strong_sell": very_strong_sell,
        "error": error,
    }
    
    return render(request, "recommendations.html", context)

def options_calculator_page(request):
    context = {
        'call': 0,
        'put': 0,
    }
    
    if request.method == "POST":
        stock = str(request.POST.get("stock"))
        strike_price = float(request.POST.get("strike_price"))
        end_date = datetime.strptime(request.POST.get("end_date"), "%Y-%m-%d").date()
        
        option = Black_Scholes(stock, strike_price, end_date)
        option.calculate_price()
        
        context = {
            'call': option.call,
            'put': option.put,
        }
        
        return render(request, "options-calculator.html", context)
    
    return render(request, "options-calculator.html", context)