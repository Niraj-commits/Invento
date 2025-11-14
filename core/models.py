from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=35,blank=False,null=False)
    address = models.CharField(max_length=25,blank=False,null=False)
    phone = models.CharField(max_length=15,blank=False,null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"