from ..models import *

def stockin_summary(user):
        StockIns = StockIn.objects.filter(created_by = user)
        Completed_stockIns = 0
        Pending_stockIns = 0
        Cancelled_stockIns = 0


        for stock in StockIns:
            if stock.status == "completed":
                Completed_stockIns += 1 
            
            elif stock.status == "pending":
                Pending_stockIns +=1
            
            elif stock.status == "cancelled":
                Cancelled_stockIns += 1
                   
        return{
        "Pending StockIns": Pending_stockIns,
        "Completed StockIns":Completed_stockIns,
        "Cancelled StockIns":Cancelled_stockIns,
        }