from django.shortcuts import render

from rest_framework import viewsets
from .models import *
from .serializer import *

class Categories(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Products(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer