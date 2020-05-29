from .model_views import StocksModelViewSet
from .api_views import StocksViewSet, StocksHistoryRsi, StocksHistoryPrice, StocksHistorySMA200
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stocks', StocksModelViewSet, basename='stocks')
router.register(r'mfi-load', StocksViewSet, basename='mfi-load')
router.register(r'history/rsi', StocksHistoryRsi, basename='stocks-history-rsi')
router.register(r'history/price', StocksHistoryPrice, basename='stocks-history-price')
router.register(r'history/sma200', StocksHistorySMA200, basename='stocks-history-sma200')
urlpatterns = router.urls
