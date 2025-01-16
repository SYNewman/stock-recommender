from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockData)
admin.site.register(Strategies)
admin.site.register(Recommendations)