from django.shortcuts import render
from .models import Stock, StockData, Strategies, Recommendations
from .app_logic import Trading_System
from datetime import datetime
from stock.calculators.options_black_scholes import Black_Scholes
from stock.calculators.kelly_criterion import Kelly_Criterion



def home_page(request):
    return render(request, "home.html")



def tutorial_page(request):
    return render(request, "tutorial.html")



def sign_up_page(request):
    return render (request, "sign_up.html")



def log_in_page(request):
    return render (request, "log_in.html")





def recommendations_page(request):
    # Update stock data
    trading_system = Trading_System.Trading_System()
    trading_system.compile_queue()
    trading_system.run_operations()
    print("All seems to be working")
    
    # Get new data
    data = Stock.objects.prefetch_related("stock_data", "strategies", "recommendations")
    return render(request, "recommendations.html", {'data': data})





def options_calculator_page(request):
    context = {
        'show_result': False,
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
            'show_result': True,
            'call': option.call,
            'put': option.put,
        }
        
        return render(request, "options-calculator.html", context)
    
    return render(request, "options-calculator.html", context)




def kelly_criterion_page(request):
    if request.method == "POST":
        trade_amount = int(request.POST.get("trade_amount"))
        trade_wins = int(request.POST.get("trade_wins"))
        average_win = float(request.POST.get("average_win"))
        average_loss = float(request.POST.get("average_loss"))
        
        calculation = Kelly_Criterion(trade_amount, trade_wins, average_win, average_loss)
        calculation.calculate_win_percent()
        calculation.calculate_win_loss_ratio()
        calculation.calculate_kelly_percent()
        
        context = {
            'show_result': True,
            'kelly_percent': calculation.k,
        }
        
        return render(request, "kelly-criterion.html", context)
    
    return render(request, "kelly-criterion.html", {'show_result':False})