from ..models import *
from .client import client_summary
from .supplier import supplier_summary
from .stockIn import stockin_summary
from .stockOut import stockout_summary
from .stockInPayment import stockinPayment_summary
from .stockOutPayment import stockoutPayment_summary

def create_dashboard(user):
        supplier_data = supplier_summary(user)
        client_data = client_summary(user)

        products = Product.objects.filter(created_by = user)
        best_seller_quantity = 0


        data={
            "Title": "Dashboard For Data of Invento",
            "Summary":{
                "Total Products":Product.objects.filter(created_by =user).count(),
                "Total Clients":client_data['client_count'],
                "Total Suppliers":supplier_data['supplier_count'],
                "Best Client":client_data['best_client'],
                "Best Supplier":supplier_data['best_supplier'],
                "Total StockOuts":client_data['total_supplied_out'],
                "Total StockIns":supplier_data['total_supplied_in']
            },
            "StockIn Status":stockin_summary(user),
            "StockOut Status":stockout_summary(user),
            "StockIn Payments":stockinPayment_summary(user),
            "StockOut Payments":stockoutPayment_summary(user)
        }
        return data