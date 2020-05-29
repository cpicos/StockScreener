from django.db import models


class Stocks(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    etoro_link = models.TextField(null=True)

    class Meta:
        db_table = 'stocks'

    def __str__(self):
        return '%', self.symbol


class StocksRsi(models.Model):
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    date_time = models.CharField(max_length=50)
    rsi_current = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    rsi_prev = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    last_refreshed = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'stocks_rsi'

    def __str__(self):
        return '% % % %', self.stock.symbol, str(self.date_time), str(self.rsi_current), str(self.rsi_prev)


class StocksPrices(models.Model):
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    date_time = models.CharField(max_length=50)
    open = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    high = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    low = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    close = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    adj_close = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    volume = models.IntegerField(null=True)

    class Meta:
        db_table = 'stocks_prices'

    def __str__(self):
        return '% % % %', self.stock.symbol, str(self.date_time), str(self.close)


class StocksSMA200(models.Model):
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    date_time = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    last_refreshed = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'stocks_sma200'

    def __str__(self):
        return '% % % %', self.stock.symbol, str(self.date_time), str(self.value)

