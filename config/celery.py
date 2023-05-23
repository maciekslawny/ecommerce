from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.schedules import crontab

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

app.conf.beat_schedule = {
    'send_payment_reminder': {
        'task': 'ecommerce.tasks.send_payment_reminder',
        'schedule': crontab(hour=8, minute=0),
    },
}

app.conf.timezone = 'UTC'

app.autodiscover_tasks()
