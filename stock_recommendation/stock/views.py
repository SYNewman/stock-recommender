# django built in features
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef
from django.contrib.auth import authenticate, login
from django.contrib import messages

# imports from this project
from .models import Stock, StockData, Strategies, Recommendations
from .hash_algorithm import Hash
from stock.calculators.options_black_scholes import Black_Scholes
from stock.calculators.kelly_criterion import Kelly_Criterion

# other modules
import datetime
from .app_logic import Trading_System
from datetime import datetime
import plotly.graph_objects as graph



def home_page(request):
    return render(request, "home.html")



def tutorial_page(request):
    return render(request, "tutorial.html")



def sign_up_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password = Hash(password) #Hash the password
        created_date_time = datetime.datetime.now()
        last_login_time = datetime.datetime.now()
        
        # code should check that the fields have been correctly filled out
        # if correctly filled out:
            # code here should create the user
            # login the user (if required)
            return redirect("recommendations")
        else:
            messages.error(request, "Please enter a valid information")
    
    return render (request, "sign_up.html")



def log_in_page(request):
    if request.method == "POST":
        #retrieve input
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password = Hash(password) #Hash the password
        last_login_time = datetime.datetime.now()
        
        user = authenticate(request, username=username, email=email, password=password, last_login_time=last_login_time)
        
        if user:
            login(request, user)
            return redirect("recommendations")
        else:
            messages.error(request, "Invalid information. Please retry")
    
    return render(request, "log_in.html")



def log_out_page(request):
    # code here should log out the user
    
    return render(request, "log_out.html")




@requires_login
def recommendations_page(request):
    # Update stock data
    trading_system = Trading_System.Trading_System()
    trading_system.compile_queue()
    trading_system.run_operations()
    
    #data = Stock.objects.prefetch_related("stock_data", "strategies", "recommendations").all() #shows stocks which don't have data - should only be used for testing
    
    # Fetches the new data
    data = Stock.objects.annotate(
        has_price=Exists( #'annotate' allows filtering of stocks shown
            StockData.objects.filter(ticker=OuterRef("pk"), current_price__isnull=False)
        ) #checks that the stock's price exists in db
    ).filter(
        company_name__isnull=False, has_price=True #Checks that the stock's company name exists
        ).prefetch_related("stock_data", "recommendations") #Links to other tables
    
    # Pagination
    paginator = Paginator(data, 100) #Shows only 100 stocks per page
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request, "recommendations.html", {'page_object': page_object})




@requires_login
def stock_info_page(request, ticker):
    #create stock chart
    stock = StockData.objects.get(ticker=ticker)
    stock_prices = stock.last_200_close_prices[0:200]
    
    figure = graph.Figure()
    scatter = graph.Scatter(y=stock_prices, mode="lines", name=f"{ticker} Prices")
    figure.add_trace(scatter)
    
    figure.update_layout(title="Stock Prices:", xaxis_title="Day", yaxis_title="Price")
    html_graph = figure.to_html(full_html=False)
    
    #gets stock data from db tables
    stock_name = get_object_or_404(Stock, ticker=ticker) # (handles error - no page shown if no data)
    stock_data = StockData.objects.filter(ticker=ticker).first()
    strategies = Strategies.objects.filter(ticker=ticker).order_by('-id').first()
    recommendations = Recommendations.objects.filter(ticker=ticker).order_by('-id').first()
    
    
    context = {
        'stock': stock_name,
        'stockData': stock_data,
        'strategies': strategies,
        'recommendations': recommendations,
        'graph': html_graph,
    }
    
    return render(request, 'stock_info.html', context)





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