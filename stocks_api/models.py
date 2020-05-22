from django.db import models


class Stocks(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return '%', self.symbol
