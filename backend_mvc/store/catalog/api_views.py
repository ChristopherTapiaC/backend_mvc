from rest_framework import viewsets
from .models import Product, Client, Sale, SaleDetail
from .serializers import ProductSerializer, ClientSerializer, SaleSerializer, SaleDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-create_in")
    serializer_class = ProductSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("-id")
    serializer_class = ClientSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by("-created_at")
    serializer_class = SaleSerializer

class SaleDetailViewSet(viewsets.ModelViewSet):
    queryset = SaleDetail.objects.all().order_by("-id")
    serializer_class = SaleDetailSerializer