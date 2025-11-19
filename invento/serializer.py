from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework import status

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','name','address','email','phone','created_at']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user

        duplicate = Client.objects.filter(name = validated_data.get('name'),address = validated_data.get('address'),phone = validated_data.get('phone')).exists()
        if duplicate :
            raise serializers.ValidationError({"Error":"Client Already Exists,Use Different Name"})
        
        validated_data['created_by'] = user
        client = Client.objects.create(**validated_data)
        return client
    
    def update(self,instance,validated_data):
        duplicate = Client.objects.filter(name = validated_data.get('name'),address = validated_data.get('address'),phone = validated_data.get('phone')).exclude(id=instance.id).exists()
        if duplicate :
            raise serializers.ValidationError({"Error":"Client Already Exists,Use Different Name"})
        
        return super().update(instance,validated_data)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id','name','address','email','phone','created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user

        duplicate = Supplier.objects.filter(name = validated_data.get('name'),address = validated_data.get('address'),phone = validated_data.get('phone')).exists()
        if duplicate :
            raise serializers.ValidationError({"Error":"Client Already Exists,Use Different Name"})
        validated_data['created_by'] = user
        client = Supplier.objects.create(**validated_data)
        return client
    
    def update(self,instance,validated_data):
        duplicate = Supplier.objects.filter(name = validated_data.get('name'),address = validated_data.get('address'),phone = validated_data.get('phone')).exclude(id=instance.id).exists()
        if duplicate :
            raise serializers.ValidationError({"Error":"Client Already Exists,Use Different Name"})
        
        return super().update(instance,validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['created_by'] = user
        category = Category.objects.create(**validated_data)
        return category

class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.StringRelatedField(source='category')
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),source="category"
    )
    image = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = ['id','name','image','description','price','quantity','category_id','category_name','created_at']
        read_only_fields = ['created_at']
    
    def create(self,validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user

        duplicate = Product.objects.filter(name=validated_data.get('name'),category = validated_data.get('category')).exists()

        if duplicate:
            raise serializers.ValidationError(detail="Product With That Name already Exists")
        validated_data['created_by'] = user
        product = Product.objects.create(**validated_data)
        return product
    
    def update(self,instance,validated_data):
        duplicate = Product.objects.filter(name=validated_data.get('name'),category = validated_data.get('category')).exclude(id=instance.id).exists()
        if duplicate:
            raise serializers.ValidationError(detail="Product Already Exists,Please Use Different Name")

        instance.name = validated_data.get('name')
        instance.image = validated_data.get('image')
        instance.description = validated_data.get('description')
        instance.price = validated_data.get('price')
        instance.quantity = validated_data.get('quantity')
        instance.category = validated_data.get('category')
        # validated data is a dictionary so we use "get" to get the key we want to access

        instance.save()
        return instance
    # alternatively
        # return super().update(instance,validated_data)

class StockInItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    product_name = serializers.StringRelatedField(source="product")
    product_id = serializers.PrimaryKeyRelatedField(source='product',queryset=Product.objects.all())
    class Meta:
        model = StockInItem
        fields = ['id','product_id','product_name','quantity','total','created_at']
        read_only_fields = ['created_at']
    
    def get_total(self,obj) -> int:
        return obj.product.price * obj.quantity
    
class StockInSerializer(serializers.ModelSerializer):
    purchased_items = StockInItemSerializer(source="stock_in_items",many=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),source = "supplier"
    )
    class Meta:
        model = StockIn
        fields = ['id','supplier_id','status','purchased_items','created_at']
        read_only_fields = ['status','created_at']
    
    def create(self, validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user
        validated_data['created_by'] = user
        item_list = validated_data.pop('stock_in_items')
        stock_in = StockIn.objects.create(**validated_data)

        for item in item_list:
            StockInItem.objects.create(stock_in=stock_in,**item)

        if stock_in.status == "completed":
            for item in stock_in.stock_in_items.select_related('product'):
                product = item.product
                product.quantity += item.quantity
                product.save()
        
        return stock_in
    
    def update(self, instance, validated_data):
        if instance.status == "completed":
            raise serializers.ValidationError({"Error":"Cannot Edit a Completed stock_in record"})
        
        item_list = validated_data.pop('stock_in_items')

        instance =  super().update(instance,validated_data)

        if item_list:
            for item in item_list:
                product = item.get['product']
                quantity = item.get['quantity']
                
                product.quantity += quantity
                product.save()

                stock_in_item = StockInItem.objects.update_or_create(stock_in = instance,product = product,quantity=quantity)
        return instance

class StockInPaymentSerializer(serializers.ModelSerializer):
    total_stock_in_value = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    stock_in_id = serializers.PrimaryKeyRelatedField(source="stock_in",queryset=StockIn.objects.all())
    amount_paid = serializers.IntegerField(source="amount")
    class Meta:
        model = StockInPayment
        fields = ['id','stock_in_id','status','total_stock_in_value','amount_paid','remaining_amount','created_at']
        read_only_fields = ['status','total_stock_in_value','remaining_amount','created_at']

    def get_total_stock_in_value(self,obj) -> int:
        return sum(
            item.product.price * item.quantity
            for item in obj.stock_in.stock_in_items.all()
        )

    def get_remaining_amount(self,obj) -> int:
        stock_in_total_value = self.get_total_stock_in_value(obj)
        return stock_in_total_value-obj.amount

    def create(self,validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user

        stock_in = validated_data.get('stock_in')
        amount = validated_data.get('amount')

        duplicate = StockInPayment.objects.filter(stock_in=stock_in).exists()

        if duplicate:
            raise serializers.ValidationError({"Error":"The Entry for this stock_out already exist"})
        validated_data['created_by'] = user

        stock_in_total = sum(
            item.product.price * item.quantity
            for item in stock_in.stock_in_items.all()
        )

        if amount > stock_in_total:
            raise serializers.ValidationError({"Error":"Paid Amount cannot exceed actual amount"})
        
        payment = StockInPayment.objects.create(**validated_data)

        if amount == 0:
            payment.status = "cancelled"
            stock_in.status = "cancelled"
            stock_in.save()
        
        elif amount > 0 and amount < stock_in_total:
            payment.status = "partial"
            stock_in.status = "pending"
            stock_in.save()
        
        elif amount == stock_in_total:
            payment.status = "paid"
            stock_in.status = "completed"
            stock_in.save()

        else:
            payment.status = "pending"
        payment.save()
        return payment
    
    def update(self, instance, validated_data):
        stock_in = instance.stock_in
        new_amount = validated_data.get('amount',0)
        total_amount = instance.amount + new_amount
        
        duplicate = StockInPayment.objects.filter(stock_in=stock_in).exclude(id=instance.id).exists()

        stock_in_total = sum(
            item.product.price * item.quantity
            for item in stock_in.stock_in_items.all()
        )
        if duplicate:
            raise serializers.ValidationError({"Error":"A Entry For that Stock is already listed"})
        if total_amount < 0 or total_amount > stock_in_total:
            raise serializers.ValidationError({"amount": "Amount must be between 0 and total stock value."})
            
        if instance.status == "paid" or stock_in.status == "completed":
            raise serializers.ValidationError({"Error":"You Cannot Edit Entries With Completed Payments"})
        
        elif instance.status == "partial":

            if total_amount < stock_in_total and total_amount > 0:
                instance.status = "partial"

            
            elif total_amount == stock_in_total:
                instance.status = "paid"
                stock_in.status = "completed"
                stock_in.save()
            
            else:
                raise serializers.ValidationError({"Error":"Unexpected Error Occured"})
        instance.amount = total_amount
        instance.save()
        return instance

class StockOutItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    product_id = serializers.PrimaryKeyRelatedField(source='product',queryset=Product.objects.all())
    product_name = serializers.StringRelatedField(source="product")
    class Meta:
        model = StockOutItem
        fields = ['id','product_id','quantity','total','product_name','created_at']
        read_only_fields = ['stock_out','created_at']

    def get_total(self,obj) -> int:
        return obj.product.price * obj.quantity

class StockOutSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    items = StockOutItemSerializer(source = "stock_out_items",many=True)
    client_name = serializers.StringRelatedField(source="client")
    client_id = serializers.PrimaryKeyRelatedField(
        queryset = Client.objects.all(),source = "client"
    )
    
    class Meta:
        model = StockOut
        fields = ['id','client_id','client_name','status','total','items','created_at']
        read_only_fields = ['status','created_at']
    
    def get_total(self,order) -> int:

        return sum (
            item.product.price * item.quantity
            for item in order.stock_out_items.all()
        )
    
    def create(self, validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user

        item_list = validated_data.pop('stock_out_items')
        validated_data['created_by'] = user
        stock_out = StockOut.objects.create(**validated_data)

        for item in item_list:
            StockOutItem.objects.create(stock_out=stock_out,**item)

        if stock_out.status == "completed":
            for item in stock_out.stock_out_items.select_related('product'):
                product = item.product

                if product.quantity < item.quantity:
                    raise serializers.ValidationError({"Error":"Item Quantity cannot exceed available products"})
                
                product.quantity -= item.quantity
                product.save()
        
        return stock_out
    
    def update(self, instance, validated_data):
        if instance.status == "completed":
            raise serializers.ValidationError({"Error":"Cannot Edit a Completed stock_out record"})
        
        item_list = validated_data.pop('stock_out_items')

        instance =  super().update(instance,validated_data)

        if item_list:
            for item in item_list:
                product = item.get['product']
                quantity = item.get['quantity']

                if product.quantity < item.quantity:
                    raise serializers.ValidationError({"Error":"Item Quantity Cannot Exceed Available Product Quantity"})
                
                product.quantity -= quantity
                product.save()

                stock_out_item = StockOutItem.objects.update_or_create(stock_out = instance,product = product,quantity=quantity)
        return instance

class StockOutPaymentSerializer(serializers.ModelSerializer):

    total_stock_out_value = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    stock_out_id = serializers.PrimaryKeyRelatedField(queryset= StockOut.objects.all(),source = "stock_out")
    class Meta:
        model = StockOutPayment
        fields= ['id','stock_out_id','amount','status','total_stock_out_value','remaining','created_at']
        read_only_fields = ['status','total_stock_out_value','remaining','created_at']

    def get_total_stock_out_value(self,obj) -> int:
        return sum(
            item.product.price * item.quantity
            for item in obj.stock_out.stock_out_items.all()
        )

    def get_remaining(self,obj) -> int:
        stock_out_total_value = self.get_total_stock_out_value(obj)
        return stock_out_total_value-obj.amount

    def create(self,validated_data):
        # Gets Currently logged in user
        request = self.context.get('request')
        user = request.user

        stock_out = validated_data.get('stock_out')
        amount = validated_data.get('amount')

        duplicate = StockOutPayment.objects.filter(stock_out=stock_out).exists()

        if duplicate:
            raise serializers.ValidationError({"Error":"The Entry for this stock_out already exist"})
        validated_data['created_by'] = user
        stock_out_total = sum(
            item.product.price * item.quantity
            for item in stock_out.stock_out_items.all()
        )

        if amount > stock_out_total:
            raise serializers.ValidationError({"Error":"Paid Amount cannot exceed actual amount"})
        
        payment = StockOutPayment.objects.create(**validated_data)

        if amount == 0:
            payment.status = "cancelled"
            stock_out.status = "cancelled"
            stock_out.save()
        
        elif amount > 0 and amount < stock_out_total:
            payment.status = "partial"
            stock_out.status = "pending"
            stock_out.save()
        
        elif amount == stock_out_total:
            payment.status = "paid"
            stock_out.status = "completed"
            stock_out.save()

        else:
            payment.status = "pending"
        payment.save()
        return payment
    
    def update(self, instance, validated_data):
        stock_out = instance.stock_out
        new_amount = validated_data.get('amount',0)
        total_amount = instance.amount + new_amount
        
        duplicate = StockOutPayment.objects.filter(stock_out=stock_out).exclude(id=instance.id).exists()

        stock_out_total = sum(
            item.product.price * item.quantity
            for item in stock_out.stock_out_items.all()
        )
        if duplicate:
            raise serializers.ValidationError({"Error":"A Entry For that Stock is already listed"})
        if total_amount < 0 or total_amount > stock_out_total:
            raise serializers.ValidationError({"amount": "Amount must be between 0 and total stock value."})
            
        if instance.status == "paid" or stock_out.status == "completed":
            raise serializers.ValidationError({"Error":"You Cannot Edit Entries With Completed Payments"})
        
        elif instance.status == "partial":

            if total_amount < stock_out_total and total_amount > 0:
                instance.status = "partial"

            
            elif total_amount == stock_out_total:
                instance.status = "paid"
                stock_out.status = "completed"
                stock_out.save()
            
            else:
                raise serializers.ValidationError({"Error":"Unexpected Error Occured"})
        instance.amount = total_amount
        instance.save()
        return instance
