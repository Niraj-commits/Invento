from .models import Notifications

def low_stock(user,message):
    Notifications.objects.create(user=user,message=message)