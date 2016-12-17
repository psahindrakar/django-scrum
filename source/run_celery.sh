#!/bin/sh

# Wait for mysql service to start
while ! nc -w 1 -z rabbitmq 5672; do sleep 5; done

# Run celery worker with circus project manager with configurations in an ini file. 
circusd circus_worker.ini