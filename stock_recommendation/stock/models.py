from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

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
    company_name = models.CharField(max_length=100, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(default=now)

# Contains the main data for each stock
class StockData(models.Model):
    ticker = models.ForeignKey(Stock,
                               on_delete=models.CASCADE,
                               related_name='stock_data',
                               db_column='ticker')
    current_date = models.DateField(null=True, blank=True)
    current_price = models.FloatField(null=True, blank=True)
    last_200_close_prices = models.JSONField(null=True, blank=True)
    price_change = models.FloatField(null=True, blank=True)
    price_change_percent = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.ticker}" #Makes string representation of object in the admin panel is primary key, not just a number
    

# Contains each strategies' signal
class Strategies(models.Model):
    ticker = models.ForeignKey(Stock,
                               on_delete=models.CASCADE,
                               related_name='strategies',
                               db_column='ticker')
    moving_averages = models.CharField(max_length=5, null=True, blank=True)
    rsi = models.CharField(max_length=5, null=True, blank=True)
    bollinger_bands = models.CharField(max_length=5, null=True, blank=True)
    
    def __str__(self):
        return f"{self.ticker}"
    

# Contains recommendation info
class Recommendations(models.Model):
    ticker = models.ForeignKey(Stock,
                               on_delete=models.CASCADE,
                               related_name='recommendations',
                               db_column='ticker')
    total_buy_signals = models.IntegerField(null=True, blank=True)
    total_hold_signals = models.IntegerField(null=True, blank=True)
    total_sell_signals = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.ticker}"