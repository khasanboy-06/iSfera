# Generated by Django 5.1.4 on 2025-01-17 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='type',
            field=models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], max_length=100),
        ),
    ]
