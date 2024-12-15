# Generated by Django 5.1.2 on 2024-12-14 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_stock_company_name_alter_stock_sector_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendations',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockdata',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recommendations',
            name='stock_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Recommendations', to='stock.stock'),
        ),
        migrations.AlterField(
            model_name='stockdata',
            name='stock_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StockData', to='stock.stock'),
        ),
    ]