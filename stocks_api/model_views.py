from .models import Stocks
from .serializers import StocksSerializer
from rest_framework import viewsets


class StocksModelViewSet(viewsets.ModelViewSet):
    queryset = Stocks.objects.all()
    serializer_class = StocksSerializer
