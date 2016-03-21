from django.core.mail import send_mail
from threading import Thread

def start_mail_thread(subject, message, sender, receivers):
    new_thread = Thread(target=send_mail, args=(subject, message, sender, receivers), kwargs={'html_message':True}, daemon=True)
    new_thread.start()
