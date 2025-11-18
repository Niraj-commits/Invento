from drf_spectacular.utils import extend_schema,OpenApiExample
from rest_framework import viewsets
from .models import *
from .serializer import *
from .pagination import *
from .custom_filter import *
from django_filters import rest_framework as filter
from .permission import *
from .utils.dashboard import *

# Customer
@extend_schema(tags=['Client'],examples=[
    OpenApiExample(
    'Simple Client Example',
    value={
        "name":"Client_Name",
        "address":"Place",
        "email":"example@example.com",
        "phone":"9786xxxxx",
    }
)])
class ClientView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = ClientFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return Client.objects.filter(created_by = self.request.user)

# Supplier
@extend_schema(tags=['Supplier'],examples=[
    OpenApiExample(
    'Simple Supplier Example',
    value={
        "name":"Supplier_Name",
        "address":"Place",
        "email":"example@example.com",
        "phone":"9786xxxxx",
    })
])
class SupplierView(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = SupplierFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return Supplier.objects.filter(created_by = self.request.user)

# Stock-In Views
@extend_schema(tags=['Category'],examples=[
    OpenApiExample(
    'Simple Category Example',
    value={
        "name":"food",
    })
])
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = CategoryFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return Category.objects.filter(created_by = self.request.user)

@extend_schema(tags=['Product'],examples=[
    OpenApiExample(
    'Simple Product Example',
    value={
        "name":"chicken",
        "description":"awesome",
        "price":50,
        "quantity":40,
        "category_id": 1
    })
])
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return Product.objects.filter(created_by = self.request.user).select_related('category')

@extend_schema(tags=['Stock-In'],examples=[
    OpenApiExample(
    'Simple Stock-In Example',
    value={
        "supplier_id":1,
        "purchased_items":[
        {
            "product_id":1,
            "quantity":5
        }
        ]
    })
])
class StockInView(viewsets.ModelViewSet):
    serializer_class = StockInSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockInFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return StockIn.objects.filter(created_by = self.request.user)

@extend_schema(tags=['Stock-In Payments'],examples=[OpenApiExample(
    'Simple Stock-In Payment Example',
    value={
        "stock_in_id":1,
        "amount":3
    }
)])
class StockInPaymentView(viewsets.ModelViewSet):
    serializer_class = StockInPaymentSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockInPaymentFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return StockInPayment.objects.filter(created_by = self.request.user)

# Stock-Out Views
@extend_schema(tags=['Stock-Out'],examples=[
    OpenApiExample(
    'Simple Stock-Out Example',
    value={
        "client_id":1,
        "items":[
        {
            "product_id":1,
            "quantity":5
        }
        ]
    })
])
class StockOutView(viewsets.ModelViewSet):
    serializer_class = StockOutSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockOutFilter
    permission_classes = [ViewPermission]

    def get_queryset(self,request):
        return StockOut.objects.filter(created_by = self.request.user)

@extend_schema(tags=['Stock-Out Payments'],examples=[OpenApiExample(
    'Simple Stock-Out Payment Example',
    value={
        "stock_out_id":1,
        "amount":3
    }
)])
class StockOutPaymentView(viewsets.ModelViewSet):
    serializer_class = StockOutPaymentSerializer
    serializer_class = StockOutPaymentSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockOutPaymentFilter
    permission_classes = [ViewPermission]

    def get_queryset(self):
        return StockOutPayment.objects.filter(created_by = self.request.user)

class DashboardView(viewsets.ViewSet):
    permission_classes = [ViewPermission]

    def list(self,request):
        data = create_dashboard(request.user)
        return Response(data)

