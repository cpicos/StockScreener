from rest_framework import viewsets
from rest_framework.response import Response


class StocksViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Get list of stocks from database
        :param request:
        :return:
        """
        print('HELLO FIRST REQUEST')
        result = []
        return Response(result)

