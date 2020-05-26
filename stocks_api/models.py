from django.db import models


class Stocks(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    etoro_link = models.TextField(null=True)

    class Meta:
        db_table = 'stocks'

    def __str__(self):
        return '%', self.symbol


class StocksInfo(models.Model):
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    date_time = models.CharField(max_length=50)
    rsi_current = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    rsi_prev = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    last_refreshed = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'stocks_info'

    def __str__(self):
        return '% % % %', self.stock.symbol, str(self.date_time), str(self.rsi_current), str(self.rsi_prev)

