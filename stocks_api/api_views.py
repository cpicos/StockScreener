from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Stocks, StocksRsi, StocksPrices
import bs4 as bs
import os
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_PORT = 2525
EMAIL_USE_TSL = True
EMAIL_HOST_USER = 'ffd3f6d9255e6c983b27c4b494533772'  # sanlygroup
EMAIL_HOST_PASSWORD = 'fb05356a370b1579c856085123b50834'


def send_simple_email():
    try:
        to_address = 'picos.rodriguez.christian@gmail.com'
        subject = 'TEST'
        message = 'HERE GOES ADVICE'
        from_address = 'SanlyGroup<sanlygroup@gmail.com>'

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        msg = MIMEMultipart()

        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print('sent')
        return 0
    except Exception as err:
        return 1


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


class StocksHistoryRsi(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Load Data From https://www.alphavantage.co/ and saving to Database
        :param request:
        :return:
        """
        api_keys = ['44GNCB5WPC55EERS', '1UOV5PHVK5K49QYS', '4V7E9U7J09JFR0SB', '7H32FTP7OP61FATO', '7RE7REQLUXM0RAH1',
                    '9RN7A9SVJOY6OSJZ', 'FYOFKJO0ED94X9WB', 'PGSQR6KMR0V0YQDF',
                    '44GNCB5WPC55EERS', '1UOV5PHVK5K49QYS', '4V7E9U7J09JFR0SB', '7H32FTP7OP61FATO', '7RE7REQLUXM0RAH1',
                    '9RN7A9SVJOY6OSJZ', 'FYOFKJO0ED94X9WB', 'PGSQR6KMR0V0YQDF',
                    ]
        # api_key = 'OS85RFN2U37I7KT9'  # gmail
        # api_keys = ['KBTBIQKOYE6IGROQ', 'LNDIK0V9C04EJM7S']
        instances = []
        # api_key = request.GET.get('api_key')

        request_counter = 0
        for api_key in api_keys:
            stocks = Stocks.objects.all()
            for stock in stocks:
                try:
                    print(stock.symbol, api_key)
                    ti = TechIndicators(key=api_key, output_format='json')
                    data_ti, meta_data_ti = ti.get_rsi(symbol=stock.symbol, interval='daily', time_period=14,
                                                       series_type='close')
                    rsi_prev = None
                    dict_items = data_ti.items()
                    sorted_items = sorted(dict_items)
                    last_refreshed = meta_data_ti.get('3: Last Refreshed')

                    for key, value in sorted_items:
                        rsi_current = value.get('RSI')
                        if not StocksRsi.objects.filter(stock=stock, date_time=key, rsi_current=rsi_current).exists():
                            instances.append(StocksRsi(stock=stock, date_time=key,
                                                        rsi_current=rsi_current,
                                                        rsi_prev=rsi_prev,
                                                        last_refreshed=last_refreshed))
                        rsi_prev = rsi_current
                    request_counter += 1

                    if request_counter % 5 == 0:
                        print('Waiting 60 seconds')
                        if len(instances) > 0:
                            StocksRsi.objects.bulk_create(instances)
                        instances = []
                        # HERE MAKE QUERY AND SEND EMAIL WITH ADVICE
                        # send_simple_email()
                        time.sleep(60)
                        # break

                except ValueError as err:
                    print(err)
            break

        result = {'data': 'Results Processed go to --> '}
        return Response(result)


class StocksHistoryPrice(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Load History Prices Data From https://www.alphavantage.co/ and saving to Database
        :param request:
        :return:
        """
        api_keys = ['44GNCB5WPC55EERS', '1UOV5PHVK5K49QYS', '4V7E9U7J09JFR0SB', '7H32FTP7OP61FATO', '7RE7REQLUXM0RAH1',
                    '9RN7A9SVJOY6OSJZ', 'FYOFKJO0ED94X9WB', 'PGSQR6KMR0V0YQDF',
                    '44GNCB5WPC55EERS', '1UOV5PHVK5K49QYS', '4V7E9U7J09JFR0SB', '7H32FTP7OP61FATO', '7RE7REQLUXM0RAH1',
                    '9RN7A9SVJOY6OSJZ', 'FYOFKJO0ED94X9WB', 'PGSQR6KMR0V0YQDF',
                    ]
        instances = []
        request_counter = 0
        for api_key in api_keys:
            stocks = Stocks.objects.all()
            for stock in stocks:
                try:
                    print(stock.symbol, api_key)
                    ts = TimeSeries(key=api_key, output_format='json')
                    data_ts, meta_data_ts = ts.get_daily_adjusted(symbol=stock.symbol, outputsize='full')
                    dict_items = data_ts.items()
                    sorted_items = sorted(dict_items)

                    for key, value in sorted_items:
                        open_price = value.get('1. open')
                        high_price = value.get('2. high')
                        low_price = value.get('3. low')
                        close_price = value.get('4. close')
                        adj_close_price = value.get('5. adjusted close')
                        volume = value.get('6. volume')
                        if not StocksPrices.objects.filter(stock=stock, date_time=key, open=open_price, high=high_price,
                                                           low=low_price, close=close_price, adj_close=adj_close_price,
                                                           volume=volume).exists():
                            instances.append(StocksPrices(stock=stock, date_time=key, open=open_price, high=high_price,
                                                          low=low_price, close=close_price, adj_close=adj_close_price,
                                                          volume=volume))
                    request_counter += 1

                    if request_counter % 5 == 0:
                        print('Waiting 60 seconds')
                        if len(instances) > 0:
                            StocksPrices.objects.bulk_create(instances)
                        instances = []
                        # HERE MAKE QUERY AND SEND EMAIL WITH ADVICE
                        # send_simple_email()
                        time.sleep(60)
                        # break
                    # break
                except ValueError as err:
                    print(err)
            break

        result = {'data': 'Results Processed go to --> '}
        return Response(result)

