#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# Run celery worker with circus project manager with configurations in an ini file. 
circusd circus_worker.ini