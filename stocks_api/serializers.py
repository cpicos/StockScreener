from .models import Stocks
from rest_framework import serializers


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ('id', 'company_name', 'symbol')
