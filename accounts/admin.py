from django.contrib import admin
from .models import *
# Register your models here.

class category(admin.ModelAdmin):
    list_display = ['id','name']
    list_editable = ['name']
    list_filter = ['name']
    search_fields = ['name']

class product(admin.ModelAdmin):
    list_display = ['id','name','cost_price','selling_price','category']
    list_editable = ['name','cost_price','selling_price']
    list_filter = ['category']
    search_fields = ['name','category']


admin.site.register(Category,category)
admin.site.register(Product,product)
admin.site.register(POS)
admin.site.register(POS_Item)
admin.site.register(GRN)
admin.site.register(Purchase_order)
admin.site.register(Purchase_Order_Item)