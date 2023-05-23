from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def payment_reminder_email(order):
    subject = 'Przypomnienie o płatności'
    html_message = render_to_string('order/payment_reminder_email.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = 'your_email@example.com'
    to_email = order.customer.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)