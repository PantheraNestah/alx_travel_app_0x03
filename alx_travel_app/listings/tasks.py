from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    subject = 'Payment Confirmation'
    message = f'Your payment for booking {booking_id} was successful. Thank you for using our service!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
