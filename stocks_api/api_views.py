from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Stocks, StocksInfo
import bs4 as bs
import glob
import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
from .serializers import StocksSerializer


class StocksViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request):
        """
        Load Data From https://www.magicformulainvesting.com/ and saving to Database
        :param request:
        :return: json
        """
        current_path = os.path.abspath(os.path.dirname(__file__))
        mfi_templates = os.path.join(current_path, "../stocks_api/mfi_templates")
        os.chdir(mfi_templates)
        # files = glob.glob('*.html')
        files = ['1.html', '2.html', '3.html', '4.html', '5.html', '6.html', '7.html', '8.html', '9.html', '10.html',
                 '11.html', '12.html', '13.html']
        result, stock_instances = self.load_data(files, mfi_templates)

        if len(stock_instances) > 0:
            Stocks.objects.bulk_create(stock_instances)
        return Response(result)

    @staticmethod
    def load_data(files, path):
        """
        Scrap data from html files
        :param files: list of strings
        :param path: relative path to templates for scrap
        :return: dictionary, instances (for bulk create)
        """
        json = []
        instances = []
        for file in files:
            f = open(os.path.join(path, file), "r")
            soup = bs.BeautifulSoup(f.read(), 'lxml')
            h1s = soup.find_all('h1')
            stock_range = h1s[1]
            range_millions = stock_range.string.split(' ')

            table = soup.find('table', class_='screeningdata')
            tbody = table.find('tbody')
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                data = {
                    'company_name': tds[0].string.strip(),
                    'symbol': tds[1].string.strip(),
                    'market_cap': tds[2].string.strip(),
                    'price_from': tds[3].string.strip(),
                    'most_recent_qtr': tds[4].string.strip(),
                    'etoro_link': 'www.etoro.com/markets/' + tds[1].string.strip() + '/chart',
                }

                if data not in json:
                    if not Stocks.objects.filter(symbol=data.get('symbol')).exists():
                        instances.append(Stocks(company_name=data.get('company_name'),
                                                symbol=data.get('symbol'),
                                                etoro_link=data.get('etoro_link')))
                    json.append(data)
        return json, instances


class StockHistory(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Load Data From https://www.alphavantage.co/ and saving to Database
        :param request:
        :return:
        """
        # api_keys = ['44GNCB5WPC55EERS', '1UOV5PHVK5K49QYS', '4V7E9U7J09JFR0SB', '7H32FTP7OP61FATO', '7RE7REQLUXM0RAH1',
        #             '9RN7A9SVJOY6OSJZ', 'FYOFKJO0ED94X9WB', 'PGSQR6KMR0V0YQDF', 'KBTBIQKOYE6IGROQ', 'LNDIK0V9C04EJM7S']
        # api_key = 'OS85RFN2U37I7KT9'  # gmail
        # api_keys = ['7H32FTP7OP61FATO']
        instances = []
        api_key = request.GET.get('api_key')

        request_counter = 0
        stocks = Stocks.objects.all()
        for stock in stocks:
            try:
                print(stock.symbol, api_key)
                ti = TechIndicators(key=api_key, output_format='json')
                data_ti, meta_data_ti = ti.get_rsi(symbol=stock.symbol, interval='30min', time_period=14,
                                                   series_type='close')
                rsi_prev = None
                dict_items = data_ti.items()
                sorted_items = sorted(dict_items)
                last_refreshed = meta_data_ti.get('3: Last Refreshed')

                for key, value in sorted_items:
                    rsi_current = value.get('RSI')
                    if not StocksInfo.objects.filter(stock=stock, date_time=key, rsi_current=rsi_current).exists():
                        instances.append(StocksInfo(stock=stock, date_time=key,
                                                    rsi_current=rsi_current,
                                                    rsi_prev=rsi_prev,
                                                    last_refreshed=last_refreshed))
                    rsi_prev = rsi_current
                request_counter += 1

                if request_counter % 5 == 0:
                    print('Waiting 60 seconds')
                    if len(instances) > 0:
                        StocksInfo.objects.bulk_create(instances)
                    instances = []
                    time.sleep(60)

            except ValueError as err:
                print(err)

        result = {'data': 'Results Processed go to --> '}
        return Response(result)
