from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('recommendations', views.recommendations_page, name='recommendations'),
    path('options-pricing-calculator', views.options_calculator_page, name='options-pricing-calculator'),
    path('sign_up', views.sign_up_page, name="sign_up_page"),
    path('log_in', views.log_in_page, name="log_in_page"),
]
