from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Order
from .scripts.payment_reminder_email import payment_reminder_email


@shared_task
def send_payment_reminder():
    payment_date = timezone.now().date() + timedelta(days=1)

    all_orders = [obj for obj in Order.objects.all() if obj.payment_date == payment_date]

    if len(all_orders) > 0:
        for order in all_orders:
            payment_reminder_email(order)
