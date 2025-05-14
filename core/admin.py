from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import *
# Register your models here.


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password","address")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","password", "address"),
            },
        ),
    )
    list_display = ["username","is_staff"]
admin.site.register(User,UserAdmin)