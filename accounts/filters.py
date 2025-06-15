
from django_filters import rest_framework as filter
from .models import *

class ProductFilter(filter.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['exact'],
        }

class SalesFilter(filter.FilterSet):
    class Meta:
        model = POS
        fields = {
            'name':['exact'],
        }

class PurchaseFilter(filter.FilterSet):
    class Meta:
        model = Purchase_order
        fields = {
            'name':['exact'],
        }