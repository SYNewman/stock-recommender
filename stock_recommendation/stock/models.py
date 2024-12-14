from django.db import models

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
    stock_id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=5, null=True)
    company_name = models.CharField(max_length=100, null=True)
    sector = models.CharField(max_length=100, null=True)
    last_updated = models.DateTimeField()

# Contains the main data for each stock
class StockData(models.Model):
    stock_id = models.ForeignKey(Stock, primary_key=True, on_delete=models.CASCADE)
    current_date = models.DateField(null=True)
    current_price = models.FloatField(null=True)
    last_200_close_prices = models.JSONField(null=True)

# Contains recommendation info
class Recommendations(models.Model):
    stock_id = models.ForeignKey(Stock, primary_key=True, on_delete=models.CASCADE)
    moving_averages_signal = models.CharField(max_length=5, null=True)
    rsi_signal = models.CharField(max_length=5, null=True)
    bollinger_bands_signal = models.CharField(max_length=5, null=True)
    overall_recommendation = models.CharField(max_length=50, null=True)