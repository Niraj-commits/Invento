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

class PointOfSale(viewsets.ModelViewSet):

    queryset = POS.objects.all()
    serializer_class = POSSerializer

class GoodReceivedNote(viewsets.ModelViewSet):

    queryset = GRN.objects.all()
    serializer_class = GRNSerializer

class ProductOrderDetail(viewsets.ModelViewSet):

    queryset = Purchase_order.objects.all()
    serializer_class = PurchaseOrderSerializer

class ProductOrderItemDetail(viewsets.ModelViewSet):

    queryset = Purchase_Order_Item.objects.all()
    serializer_class = Purchase_Order_Item_Serializer