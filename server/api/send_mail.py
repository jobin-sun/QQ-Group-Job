from threading import Thread
from base64 import b64encode
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from smtplib import SMTP
from django.conf import settings

def start_mail_thread(subject, message, receivers):
    c = charset.Charset()
    c.header_encoding = charset.BASE64
    c.body_encoding = charset.BASE64
    # c.input_charset = 'utf-8'

    msg = MIMEText(message, 'html', 'utf-8')
    h = Header(subject, c)
    sender = settings.DEFAULT_FROM_EMAIL
    msg['Subject'] = h
    msg['From'] = "=?utf-8?b?%s?= <%s>" % (b64encode("QJob社交招聘".encode("utf-8")).decode("utf-8"), sender)
    msg['To'] = ','.join(receivers)

    smtp = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.login(settings.EMAIL_HOST_USER, sender)

    new_thread = Thread(target=smtp.sendmail, args=[settings.DEFAULT_FROM_EMAIL, receivers, msg.as_string()], daemon=True)
    new_thread.start()
