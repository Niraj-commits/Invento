from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']

    def create(self, validated_data):
        occurence = Category.objects.filter(name = validated_data.get('name')).exists()
        if occurence:
            raise serializers.ValidationError({"detail":"categories cannot have same name"})
        category = self.Meta.model(**validated_data) #as the condition is true creatin new data
        category.save()
        return category
    
    def update(self,instance,validated_data):

        new_name = validated_data.get('name')

        if instance.name != new_name: #checking if name is changed
            duplicate = Category.objects.filter(name = new_name).exclude(pk = instance.pk).exists()
            if duplicate:
                raise serializers.ValidationError({"detail":"Category with that name already exists"})
    
        instance.name = validated_data.get('name')
        instance.save()
        return instance
    
        # OR for multiple values
        # for attr,values in validated_data.items():
        #     setattr(instance,attr,values)
        # instance.save()
        # return instance

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','name','description','cost_price','selling_price','category']

    def create(self,validated_data):
        duplicate = Product.objects.filter(name = validated_data.get('name'),category = validated_data.get('category')).exists()

        if duplicate:
            raise serializers.ValidationError({"Detail":"Duplicate Products in same category"})
        
        product = self.Meta.model(**validated_data)
        product.save()
        return product
    
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