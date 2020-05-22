from .model_views import StocksModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stocks', StocksModelViewSet, basename='stocks')
urlpatterns = router.urls
