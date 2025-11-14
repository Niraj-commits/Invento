from django.db import models
from core.models import User
# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=25,blank=True,null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(unique=True,blank=False,null=False)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=25,blank=True,null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(unique=True,blank=False,null=False)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=55)
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField()
    image = models.ImageField(upload_to='products/',null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class StockOut(models.Model):
    status_choice = (('pending','pending'),('completed','completed'),('cancelled','cancelled'),)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    status = models.CharField(max_length=25,choices=status_choice,default="pending")
    status = models.CharField(max_length=255,choices=status_choice,default="pending")
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

    @property
    def total(self):
        return sum(
            item.product.price * item.quantity
            for item in self.stock_out_items.all()
        )
    def __str__(self):
        return f"StockOut-{self.id}, Total = {self.total} Rupees"

class StockOutItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name="stock_out_products")
    stock_out = models.ForeignKey(StockOut,on_delete=models.PROTECT,related_name="stock_out_items")
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

class StockOutPayment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('cancelled','cancelled'),
        ('partial','partial'),
    )
    stock_out = models.OneToOneField(StockOut,on_delete=models.CASCADE,related_name='stock_out_payment')
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=25,choices=PAYMENT_STATUS,default="pending")
    status = models.CharField(max_length=255,choices=PAYMENT_STATUS,default="pending")
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

class StockIn(models.Model):
    status_choices = (('pending','pending'),('completed','completed'),('cancelled','cancelled'),)
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT)
    status = models.CharField(max_length=25,choices=status_choices,default="pending")
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT,related_name="orders")
    status = models.CharField(max_length=255,choices=status_choices,default="pending")
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)

    @property
    def total(self):
        return sum(
            item.product.price * item.quantity
            for item in self.stock_in_items.all()
        )
    def __str__(self):
        return f"StockIn- {self.id}, Total = {self.total}"

class StockInItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name="stock_in_products")
    stock_in = models.ForeignKey(StockIn,on_delete=models.PROTECT,related_name='stock_in_items')
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

class StockInPayment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('cancelled','cancelled'),
        ('partial','partial'),
    )
    stock_in = models.OneToOneField(StockIn,on_delete=models.CASCADE,related_name='stock_in_payment')
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=25,choices=PAYMENT_STATUS,default="pending")
    status = models.CharField(max_length=255,choices=PAYMENT_STATUS,default="pending")
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)