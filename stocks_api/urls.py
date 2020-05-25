from .model_views import StocksModelViewSet
from .api_views import StocksViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stocks', StocksModelViewSet, basename='stocks')
router.register(r'load', StocksViewSet, basename='stocks-load')
urlpatterns = router.urls
