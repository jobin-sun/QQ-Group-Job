from threading import Thread
from base64 import b64encode
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from smtplib import SMTP
from django.conf import settings

def start_mail_thread(subject, message, sender, receivers):
    c = charset.Charset()
    c.header_encoding = charset.BASE64
    c.body_encoding = charset.BASE64
    # c.input_charset = 'utf-8'

    msg = MIMEText(message, 'html', 'utf-8')
    h = Header(subject, c)
    msg['Subject'] = h
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    smtp = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    new_thread = Thread(target=smtp.sendmail, args=[sender, receivers, msg.as_string()], daemon=True)
    new_thread.start()
