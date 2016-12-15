from celery import shared_task

@shared_task
def say_hi():
    print('[Celery task] Saying hi from celery')
    