
from django_filters import rest_framework as filter
from .models import *

class ProductFilter(filter.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['exact'],
            'category':['exact'],
        }

class SalesFilter(filter.FilterSet):
    class Meta:
        model = POS
        fields = {
            'customer':['exact'],
        }

class PurchaseFilter(filter.FilterSet):
    class Meta:
        model = Purchase_order
        fields = {
            'supplier':['exact'],
        }

class GRNFilter(filter.FilterSet):
    class Meta:
        model = GRN
        fields = {
            'product':['exact'],
        }

class CategoryFilter(filter.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name':['exact'],
        }