from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id','name']
        model = Category

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id','name','description','cost_price','selling_price','category']
        model = Product
    
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id','methods']
        model = Payment

class POSSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','product','payment']
        model = POS

class GRNSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','product','payment']
        model = GRN

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','user','status']
        model = Purchase_order

class Purchase_Order_Item_Serializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','product','order','quantity']
        model = Purchase_Order_Item