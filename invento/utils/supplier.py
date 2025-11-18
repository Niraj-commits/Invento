from ..models import *

def supplier_summary(user):
        suppliers = Supplier.objects.filter(created_by = user)
        supplier_count = suppliers.count()

        best_supplier_supplied = 0
        best_supplier = ""
        
        for supplier in suppliers:
            final_value = 0
            for stock_ins in supplier.stockin.all():
                 if stock_ins.status == "completed":
                      final_value += 1
            
            if final_value > best_supplier_supplied:
                best_supplier_supplied = final_value
                best_supplier = supplier.name
        total_supplied_in = sum(
            item.quantity
            for supplier in suppliers
            for stock_in in supplier.stockin.all()
            for item in stock_in.stock_in_items.all()
        )
        
        return {
            "total_supplied_in":total_supplied_in,
            "supplier_count":supplier_count,
            "best_supplier":best_supplier
        }