import datetime as dt
from .models import Stocks
from rest_framework import serializers
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time


class StocksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stocks
        fields = ('id', 'company_name', 'symbol', 'etoro_link')

