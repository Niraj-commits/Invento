from ..models import *

def stockoutPayment_summary(user):
        StockOutPayments = StockOutPayment.objects.filter(created_by = user)
        Cancelled_Payments = 0
        Partial_Payments = 0
        Pending_Payments = 0
        Paid_Payments = 0

        for payments in StockOutPayments:
            if payments.status == "paid":
                Paid_Payments += 1 
            
            elif payments.status == "pending":
                Pending_Payments +=1
            
            elif payments.status == "cancelled":
                Cancelled_Payments += 1
            
            elif payments.status == "partial":
                 Partial_Payments += 1
                   
        return{
        "Cancelled_Payments":Cancelled_Payments,
        "Partial_Payments":Partial_Payments,
        "Pending_Payments":Pending_Payments,
        "Paid_Payments":Paid_Payments
        }