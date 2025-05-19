# django built in features
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
        
        # Over here should be the code for multiple fields. Change it later
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("recommendations")
    else:
        form = UserCreationForm()
            
    return render(request, "sign_up.html", {"form": form})



def log_in_page(request):
    if request.method == "POST":
        #retrieve input
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        last_login_time = datetime.now()
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("recommendations")
        else:
            messages.error(request, "Invalid information. Please retry")
    
    return render(request, "log_in.html")



def log_out_page(request):
    logout(request)
    return redirect("home_page")




@login_required
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




@login_required
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
        # Get data which is entered
        stock = str(request.POST.get("stock"))
        strike_price = float(request.POST.get("strike_price"))
        end_date = datetime.strptime(request.POST.get("end_date"), "%Y-%m-%d").date()
        
        # Processes the data
        option = Black_Scholes(stock, strike_price, end_date)
        option.calculate_price()
        
        context = {
            'show_result': True,
            'call': option.call,
            'put': option.put,
        }
        
        # Reload the page, now with the options prices
        return render(request, "options-calculator.html", context)
    
    return render(request, "options-calculator.html", context)




def kelly_criterion_page(request):
    if request.method == "POST":
        # Get data which is entered
        trade_amount = int(request.POST.get("trade_amount"))
        trade_wins = int(request.POST.get("trade_wins"))
        average_win = float(request.POST.get("average_win"))
        average_loss = float(request.POST.get("average_loss"))
        
        # Processes the data
        calculation = Kelly_Criterion(trade_amount, trade_wins, average_win, average_loss)
        calculation.calculate_win_percent()
        calculation.calculate_win_loss_ratio()
        calculation.calculate_kelly_percent()
        
        context = {
            'show_result': True,
            'kelly_percent': calculation.k,
        }
        
        # Reload the page, now with the result of the calculation
        return render(request, "kelly-criterion.html", context)
    
    return render(request, "kelly-criterion.html", {'show_result':False})