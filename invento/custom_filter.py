from django_filters import rest_framework as filter
from .models import *

class CategoryFilter(filter.FilterSet):
    class Meta:
        model = Category
        fields ={
                "name":['icontains']
            }

class ProductFilter(filter.FilterSet):

    category = filter.CharFilter(field_name="category__name",lookup_expr="icontains")
    class Meta:
        model = Product
        fields = {
            "name":['icontains'],
            "category":['exact'],
            "price":['lte','gte'],
        }

class StockInFilter(filter.FilterSet):
    supplier = filter.CharFilter(field_name="supplier__name",lookup_expr="icontains")
    class Meta:
        model = StockIn
        fields = {
            "status":['exact'],
            "supplier":['exact'],
        }

class StockOutFilter(filter.FilterSet):
    client = filter.CharFilter(field_name="client__name",lookup_expr="icontains")
    class Meta:
        model = StockOut
        fields = {
            "status":['exact'],
            "client":['exact'],
        }

class StockInPaymentFilter(filter.FilterSet):
    class Meta:
        model = StockInPayment
        fields = {
            "status":['exact']
        }

class StockOutPaymentFilter(filter.FilterSet):
    class Meta:
        model = StockOutPayment
        fields = {
            "status":['exact']
        }

class SupplierFilter(filter.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            "name":['icontains'],
            "address":['icontains']
        }

class ClientFilter(filter.FilterSet):
    class Meta:
        model = Client
        fields = {
            "name":['icontains'],
            "address":['icontains']
        }