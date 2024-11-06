from django.db import models

# Each class is a model. A model is a table in the database.

# Model for the Stock table
# Contains basic information about each stock
class Stock(models.Model):
    stock_id = models. #(Primary Key, unique identifier for each stock)
    ticker = models.CharField(max_length=5)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    last_updated = models.DateTimeField()

# Model for the Stock Data table
# Contains the main data for each stock
class StockData(models.Model):
    #stock_id
    pass

# Model for the Recommendations table
# Contains the stocks which are recommended and relevant data
class Recommendations(models.Model):
    pass

#Model for the Users table
#Contains information about the users
class Users(models.Model):
    pass
