from .model_views import StocksModelViewSet
from .api_views import StocksViewSet, StockHistory
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stocks', StocksModelViewSet, basename='stocks')
router.register(r'mfi-load', StocksViewSet, basename='mfi-load')
router.register(r'history', StockHistory, basename='stocks-history')
urlpatterns = router.urls
