from django.db import models
from core.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)

class Product(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    cost_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Payment(models.Model):
    payment_methods = [('esewa','esewa'),('khalti','khalti'),('cash','cash')]
    methods = models.CharField(max_length=15,choices=payment_methods,default="cash")

class POS(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)

class POS_Item(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    sales_id = models.ForeignKey(POS,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Purchase_order(models.Model):
    order_status = [('pending','pending'),('completed','completed'),('cancelled','cancelled')]
    supplier = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=25,choices=order_status,default="pending")

class Purchase_Order_Item(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Purchase_order,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class GRN(models.Model):
    purchase_order = models.ForeignKey(Purchase_order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)

