#!/bin/sh
echo Start Script
export UBOX_ADMIN=""
export SERVER_NAME=""
export MAIL_USERNAME="tony.vuhoang178@gmail.com"
export MAIL_PASSWORD=""
gunicorn -b unix:ubox.sock -w 3 -k 'eventlet' manage:app
