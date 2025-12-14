from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, ClientViewSet, SaleViewSet, SaleDetailViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'sales', SaleViewSet, basename='sales')
router.register(r'saledetails', SaleDetailViewSet, basename='saledetails')

urlpatterns = [
    path('', include(router.urls)),
]
