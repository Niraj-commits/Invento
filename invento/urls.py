from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("category",CategoryView,basename="category")
router.register("product",ProductView,basename="product")

router.register("client",ClientView,basename="client")
router.register("supplier",SupplierView,basename="supplier")

router.register("stock-ins",StockInView,basename="stockin")
# router.register("stock-in-items",StockInItemView,basename="stockinitem")

router.register("stock-outs",StockOutView,basename="stockout")
# router.register("stock-out-items",StockOutItemView,basename="stockoutitem")

router.register("payment/stock-out-payments",StockOutPaymentView,basename="stockoutpayment")
router.register("payment/stock-in-payments",StockInPaymentView,basename="stockinpayment")

router.register("dashboard",DashboardView,basename="dashboard")

urlpatterns = [
    path('',include(router.urls)),
]