# Generated by Django 3.0.6 on 2020-05-22 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='stocks',
            table='stock',
        ),
    ]
