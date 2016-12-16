from celery.schedules import crontab
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrum.settings")

from django.conf import settings
from celery import Celery  
from .tasks import say_hi

app = Celery('scrum', backend='amqp', broker='amqp://rabbit_admin:scrum@2016!@rabbitmq//?heartbeat=30')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'scrum.tasks.say_hi',
        'schedule': crontab(minute='*')
    },
}