from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Stocks
import bs4 as bs
import glob
import os


class StocksViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Load Data From https://www.magicformulainvesting.com/
        :param request:
        :return:
        """
        result = []
        current_path = os.path.abspath(os.path.dirname(__file__))
        mfi_templates = os.path.join(current_path, "../stocks_api/mfi_templates")
        os.chdir(mfi_templates)
        stock_instances = []
        # files = glob.glob('*.html')
        files = ['1.html', '2.html', '3.html', '4.html', '5.html', '6.html', '7.html', '8.html', '9.html', '10.html',
                 '11.html', '12.html', '13.html']
        print(files)
        for file in files:
            f = open(os.path.join(mfi_templates, file), "r")
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

                if data not in result:
                    if not Stocks.objects.filter(symbol=data.get('symbol')).exists():
                        stock_instances.append(Stocks(company_name=data.get('company_name'),
                                                      symbol=data.get('symbol'),
                                                      etoro_link=data.get('etoro_link')))
                    result.append(data)
        if len(stock_instances) > 0:
            Stocks.objects.bulk_create(stock_instances)
        return Response(result)

