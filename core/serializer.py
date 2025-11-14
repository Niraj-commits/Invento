from rest_framework import serializers
from .models import *

# Login 
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']

class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','address','phone','created_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password','address','phone','created_at']
        read_only_fields = ['created_at']