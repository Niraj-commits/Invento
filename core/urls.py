from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("register",RegisterView,basename="register")
router.register("login",Login,basename="login")
router.register("users",ViewUsers,basename="users")

urlpatterns = [
    path('',include(router.urls)),
]
