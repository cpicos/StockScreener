from django.db import models


class Stocks(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    etoro_link = models.TextField(null=True)

    class Meta:
        db_table = 'stocks'

    def __str__(self):
        return '%', self.symbol
