import os

from celery import Celery  
from django.conf import settings

CELERY_TIMEZONE = 'UTC'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrum.settings")

app = Celery('scrum', broker='amqp://rabbit_admin:scrum@2016!@rabbitmq//?heartbeat=30')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)