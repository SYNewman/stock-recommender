from django.db import models

# Each class is a model. A model is a table in the database.

# Model for the Stock table
# Contains basic information about each stock
class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    last_updated = models.DateTimeField()