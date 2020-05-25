import datetime as dt
from .models import Stocks
from rest_framework import serializers
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time


class StocksSerializer(serializers.ModelSerializer):
    rsi = serializers.SerializerMethodField()

    class Meta:
        model = Stocks
        fields = ('id', 'company_name', 'symbol', 'etoro_link', 'rsi')

    @staticmethod
    def get_rsi(symbol, api_key):
        api_keys = ['', '', '', '', '', '', '', '', '', '']
        # api_key = 'OS85RFN2U37I7KT9'  # gmail

        try:
            # ts = TimeSeries(key=api_key, output_format='pandas')
            # data, meta_data = ts.get_intraday(symbol=obj.symbol, interval='60min', outputsize='full')
            ti = TechIndicators(key=api_key, output_format='pandas')
            data_ti, meta_data_ti = ti.get_rsi(symbol=symbol, interval='60min', time_period=14, series_type='close')
            print(data_ti)
        except Exception as err:
            print('OBTENER EL SIGUIENTE INDICE DE LAS LLAVES')
        return 'RSI'
