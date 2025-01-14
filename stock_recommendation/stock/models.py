from django.db import models
from django.utils.timezone import now

#Contains information about each user
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_date_time = models.DateTimeField()
    last_login_time = models.DateTimeField()
    
# Contains basic information about each stock
class Stock(models.Model):
    ticker = models.CharField(max_length=5, primary_key=True)
    company_name = models.CharField(max_length=100, null=True)
    sector = models.CharField(max_length=100, null=True)
    last_updated = models.DateTimeField(default=now)

# Contains the main data for each stock
class StockData(models.Model):
    ticker = models.ForeignKey(Stock,
                               on_delete=models.CASCADE,
                               related_name='stockData',
                               db_column='ticker')
    current_date = models.DateField(null=True)
    current_price = models.FloatField(null=True)
    last_200_close_prices = models.JSONField(null=True)

# Contains each strategies' signal
class Strategies(models.Model):
    ticker = models.ForeignKey(Stock,
                               on_delete=models.CASCADE,
                               related_name='strategies',
                               db_column='ticker')
    moving_averages = models.CharField(max_length=5, null=True)
    rsi = models.CharField(max_length=5, null=True)
    bollinger_bands = models.CharField(max_length=5, null=True)

# Contains recommendation info
class Recommendations(models.Model):
    ticker = models.ForeignKey(Stock,
                               on_delete=models.CASCADE,
                               related_name='recommendations',
                               db_column='ticker')
    total_buy_signals = models.IntegerField(default=0)
    total_hold_signals = models.IntegerField(default=0)
    total_sell_signals = models.IntegerField(default=0)