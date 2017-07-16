#!/bin/sh
echo starting celery
export SERVER_NAME=""
export MAIL_USERNAME=""
export MAIL_PASSWORD=""
celery -A app.celery_worker.celery worker --loglevel=INFO

