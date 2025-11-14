from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def Stock_Out_Completed(email,username):
    send_mail(
        subject="Stock-Out Completed",
        message=f"Hello! {username} your stock_out process is completed",
        recipient_list=[email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False
    )