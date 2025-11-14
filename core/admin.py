from django.contrib import admin
from .models import User
# Register your models here.
from django.contrib.auth.admin import UserAdmin

class CustomUser(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password",'email','address','phone')}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","password1",'password2','email','is_staff','address','phone'),
            },
        ),
    )

    list_display = ['username','email','address','phone']
    list_editable = ['email','address','phone']
    search_fields = ['username']
    list_per_page = 5

admin.site.register(User,CustomUser)