from django.db import models

# Each class is a model. A model is a table in the database.

#Model for the Users table
#Contains information about the users
class Users(models.Model):
    pass

# Model for the Stock table
# Contains basic information about each stock
class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=5)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    last_updated = models.DateTimeField()

# Model for the Stock Data table
# Contains the main data for each stock
class StockData(models.Model):
    data_id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.IntegerField()

# Model for the Recommendations table
# Contains the stocks which are recommended and relevant data
class Recommendations(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=100)
    generated_time = models.DateTimeField()