from smtplib import SMTP
from email.mime.text import MIMEText

def send_code(user, code):
    subject = 'Qjob: email confirmation'
    sender = ''
    smtpserver = ''
    username = ''
    password = ''

    msg = MIMEText('%s' % code, 'utf-8')

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = user.email

    smtp = SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, user.email, msg.as_string())

    smtp.quit()
