from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockDataViewSet

router = DefaultRouter()
router.register(r'stock-data', StockDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]