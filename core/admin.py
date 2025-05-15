from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUser(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password",'phone','role','company_name')}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","password",'phone','role','company_name'),
            },
        ),
    )
    list_display = ['id','username','role','company_name']
    list_filter = ['role']
    search_fields = ['username','role']

admin.site.register(User,CustomUser)