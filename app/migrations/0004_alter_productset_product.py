# Generated by Django 5.1.4 on 2025-01-17 06:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productset',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sets', to='app.product'),
        ),
    ]
