from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from app import celery


@celery.task
def send_async_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    send_async_email.delay(to, subject, template, **kwargs)
