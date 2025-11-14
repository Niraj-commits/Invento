from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email,username):
    send_mail(
        subject = 'Welcome To Invento!!!',
        message = f'hi {username},\n\nThank You For Joining Invento!!',
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [email],
        fail_silently=False
    )