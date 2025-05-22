from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'category',Categories,basename="category"),
router.register(r'product',Products,basename="product"),
router.register(r'sales',PointOfSale,basename="sales"),
router.register(r'purchase',GoodReceivedNote,basename="purchase"),
router.register(r'order',ProductOrderDetail,basename="order"),
router.register(r'order_item',ProductOrderItemDetail,basename="order_item"),

urlpatterns = [
    path('',include(router.urls)),
]
