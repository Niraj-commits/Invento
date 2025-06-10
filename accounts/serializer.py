from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','name','description','cost_price','selling_price','category']
    
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id','methods']
        model = Payment

class SalesItemSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id','product','sales_id','quantity']
        model = POS_Item

class POSSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer()
    items = SalesItemSerializer(many = True)

    class Meta:
        fields = ['id','items','payment']
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