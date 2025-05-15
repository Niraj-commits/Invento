from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role_options = [('admin','admin'),('customer','customer'),('supplier','supplier')]

    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=15,choices=role_options,default="customer")
    company_name = models.CharField(max_length=35)

