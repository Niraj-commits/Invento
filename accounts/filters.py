
from django_filters import rest_framework as filter
from .models import *

class CustomFilter(filter.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['exact'],
        }