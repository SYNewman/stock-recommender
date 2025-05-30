# Generated by Django 5.1.2 on 2025-01-08 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('ticker', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('sector', models.CharField(max_length=100, null=True)),
                ('last_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_date_time', models.DateTimeField()),
                ('last_login_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_buy_signals', models.IntegerField()),
                ('total_hold_signals', models.IntegerField()),
                ('total_sell_signals', models.IntegerField()),
                ('ticker', models.ForeignKey(db_column='ticker', on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='stock.stock')),
            ],
        ),
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField(null=True)),
                ('current_price', models.FloatField(null=True)),
                ('last_200_close_prices', models.JSONField(null=True)),
                ('ticker', models.ForeignKey(db_column='ticker', on_delete=django.db.models.deletion.CASCADE, related_name='stockData', to='stock.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Strategies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moving_averages', models.CharField(max_length=5, null=True)),
                ('rsi', models.CharField(max_length=5, null=True)),
                ('bollinger_bands', models.CharField(max_length=5, null=True)),
                ('ticker', models.ForeignKey(db_column='ticker', on_delete=django.db.models.deletion.CASCADE, related_name='strategies', to='stock.stock')),
            ],
        ),
    ]
