from drf_spectacular.utils import extend_schema,OpenApiExample
from rest_framework import viewsets
from .models import *
from .serializer import *
from .pagination import *
from .custom_filter import *
from django_filters import rest_framework as filter
from .permission import *

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
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ViewPermission]
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = ClientFilter

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
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = SupplierFilter
    permission_classes = [ViewPermission]

# Stock-In Views
@extend_schema(tags=['Category'],examples=[
    OpenApiExample(
    'Simple Category Example',
    value={
        "name":"food",
    })
])
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = CategoryFilter
    permission_classes = [ViewPermission]

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
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [ViewPermission]

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
    queryset = StockIn.objects.all()
    serializer_class = StockInSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockInFilter
    permission_classes = [ViewPermission]

@extend_schema(tags=['Stock-In Payments'],examples=[OpenApiExample(
    'Simple Stock-In Payment Example',
    value={
        "stock_in_id":1,
        "amount":3
    }
)])
class StockInPaymentView(viewsets.ModelViewSet):
    queryset = StockInPayment.objects.all()
    serializer_class = StockInPaymentSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockInPaymentFilter
    permission_classes = [ViewPermission]

# Stock-Out Views
@extend_schema(tags=['Stock-Out'],examples=[
    OpenApiExample(
    'Simple Stock-Out Example',
    value={
        "customer_id":1,
        "purchased_items":[
        {
            "product_id":1,
            "quantity":5
        }
        ]
    })
])
class StockOutView(viewsets.ModelViewSet):
    queryset = StockOut.objects.select_related('client')
    serializer_class = StockOutSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockOutFilter
    permission_classes = [ViewPermission]

@extend_schema(tags=['Stock-Out Payments'],examples=[OpenApiExample(
    'Simple Stock-Out Payment Example',
    value={
        "stock_out_id":1,
        "amount":3
    }
)])
class StockOutPaymentView(viewsets.ModelViewSet):
    queryset = StockOutPayment.objects.all()
    serializer_class = StockOutPaymentSerializer
    serializer_class = StockOutPaymentSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockOutPaymentFilter
    permission_classes = [ViewPermission]

class DashboardView(viewsets.ViewSet):
    best_supplier = ""
    best_client = ""
    total_revenue = 0
    best_seller = ""

    def list(self,request):
        total_products = Product.objects.count()
        items_bought = StockIn.objects.count()
        items_sold = StockOut.objects.count()
        suppliers = Supplier.objects.all()
        clients = Client.objects.all()

        product_supplied_in = 0

        for supplier in suppliers:
            total_products = 0
            for order in supplier.orders.all():
                for items in order.stock_in_items.all():
                    total_products += items.quantity

        data= {
            "total_products":total_products,
            "total_stock_in":items_bought,
            "total_stock_out":items_sold,
        }
        return Response(data)

