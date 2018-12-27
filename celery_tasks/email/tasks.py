from celery_tasks.main import celery_app
from flask import Flask, render_template, current_app
from flask_mail import Mail, Message
from .config import config

app = Flask(__name__)
app.config.from_object(config)
mail = Mail(app)

print("init task")
print(app.config['FLASKY_MAIL_SUBJECT_PREFIX'])


@celery_app.task(name='send_email')
def send_email(to, subject, template, **kwargs):
    with app.app_context():
        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
        print('aaa')
