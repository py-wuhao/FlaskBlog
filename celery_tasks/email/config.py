import os


class config(object):
    # ----------配置email-----------------------
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '17762392194@163.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '15392746632@qq.com'

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'wh123321'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '17762392194@163.com'
