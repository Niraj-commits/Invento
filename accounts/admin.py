from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(POS)
admin.site.register(POS_Item)
admin.site.register(GRN)
admin.site.register(Purchase_order)
admin.site.register(Purchase_Order_Item)