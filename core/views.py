from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .models import *
from .serializer import *
from .permission import *
from drf_spectacular.utils import extend_schema,OpenApiExample
from .email_task import send_welcome_email

class Login(viewsets.ViewSet):
    @extend_schema(
        tags=['Auth'],
        request=LoginSerializer,
        responses={200: LoginSerializer},
        examples=[
            OpenApiExample(
                'Simple Login Example',
                value={
                    "username":"username",
                    "password":"password",
                },
            )
        ]
    )
    def create(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username == None and password == None:
            raise serializers.ValidationError(detail="Username or Password Field Cannot be empty",status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user = authenticate(username = username,password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user":username,
            })
        else:
            return Response({"Error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)

class RegisterView(viewsets.ViewSet):
    @extend_schema(
        tags=['Auth'],
        request=RegisterSerializer,
        responses={201:RegisterSerializer},
        examples=[OpenApiExample(
            'Simple Register Example',
            value={
                "username":"username",
                "password":"password",
                "address":"address",
                "email":"email@example.com",
                "phone":"98xxxxx",
            },
        )]
    )
    def create(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message":"Registration Successful",
                "username":user.username,
                "email":user.email,
            },status=status.HTTP_201_CREATED)
        send_welcome_email.delay(user.email,user.username)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['View Users'])
class ViewUsers(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ViewUserSerializer
    permission_classes = [ViewUserPermission]