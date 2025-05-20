from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id','name']
        model = Category