from __future__ import absolute_import

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrum.settings")
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import *

from celery import shared_task


@shared_task
def say_hi():
    print('[Celery task] Saying hi from celery')


@shared_task
def send_welcome_email():
    # After trying whole lot of things to get the Sendgrid API from setting or from and env file, it could not be done. So until there is way to 
    # get it here from outside, keeping it hardcoded. No choice. 
    SENDGRID_KEY = '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'
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_KEY)
    from_email = Email("no-reply@selenite.co")
    subject = "Welcome to Selenite"
    to_email = Email("psahindrakar@gmail.com")
    content = Content("text/plain", "Hello Pratik, Welcome to Selenite")
    mail = Mail(from_email, subject, to_email, content)
    
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except OSError as err:
        print('Something horrible went wrong: ' + str(err))
    
    