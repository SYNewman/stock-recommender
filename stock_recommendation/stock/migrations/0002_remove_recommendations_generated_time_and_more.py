# Generated by Django 5.1.2 on 2024-12-02 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendations',
            name='generated_time',
        ),
        migrations.RemoveField(
            model_name='recommendations',
            name='recommendation_id',
        ),
        migrations.RemoveField(
            model_name='recommendations',
            name='recommendation_type',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='close_price',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='data_id',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='date',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='high_price',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='low_price',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='open_price',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='volume',
        ),
        migrations.AddField(
            model_name='recommendations',
            name='bollinger_bands_signal',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='recommendations',
            name='moving_averages_signal',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='recommendations',
            name='overall_recommendation',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='recommendations',
            name='rsi_signal',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='stockdata',
            name='current_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='stockdata',
            name='current_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stockdata',
            name='last_200_close_prices',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='recommendations',
            name='stock_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock.stock'),
        ),
        migrations.AlterField(
            model_name='stockdata',
            name='stock_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock.stock'),
        ),
    ]
