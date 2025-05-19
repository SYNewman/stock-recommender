from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"), #Home page
    path('tutorial', views.tutorial_page, name='tutorial'),
    
    #Main app
    path('recommendations', views.recommendations_page, name='recommendations'),
    path('stock/<str:ticker>', views.stock_info_page, name="stock_info"),
    
    #Calculators
    path('options-pricing-calculator', views.options_calculator_page, name='options-pricing-calculator'),
    path('kelly-criterion', views.kelly_criterion_page, name="kelly-criterion"),
    
    #Authentication
    path('sign_up', views.sign_up_page, name="sign_up_page"),
    path('log_in', views.log_in_page, name="log_in_page"),
    path('log_out', views.log_out_page, name="log_out_page"),
    #this is for redirecting when a non-signed-in user is trying to access a protected page:
    path('accounts/login/', views.log_in_page, name="other_login"),
]
