from ..models import *

def stockout_summary(user):
        clients = Client.objects.filter(created_by = user)
        StockOuts = StockOut.objects.filter(created_by = user)
        Completed_stockOuts = 0
        Pending_stockOuts = 0
        Cancelled_stockOuts = 0


        for stock in StockOuts:
            if stock.status == "completed":
                Completed_stockOuts += 1
            elif stock.status == "pending":
                Pending_stockOuts += 1
            elif stock.status == "cancelled":
                Cancelled_stockOuts += 1
                   
        return {
        "Pending StockOuts": Pending_stockOuts,
        "Completed StockOuts":Completed_stockOuts,
        "Cancelled StockOuts":Cancelled_stockOuts,
        }