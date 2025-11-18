from ..models import *

def client_summary(user):
        clients = Client.objects.filter(created_by = user)
        client_count = clients.count()

        best_client_value = 0
        best_client = ""
        
        for client in clients:
            total_value = 0
            for stock_outs in client.stockout.all():
                if stock_outs.status == "completed":
                    total_value += 1
            
            if total_value > best_client_value:
                best_client_value = total_value
                best_client = client.name

        total_supplied_out = sum(
            item.quantity
            for client in clients
            for stock_out in client.stockout.all()
            for item in stock_out.stock_out_items.all()
        )
        return{
            "client_count":client_count,
            "total_supplied_out":total_supplied_out,
            "best_client" : best_client
            }