# utils/custom_email_backend.py
import smtplib
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class CustomEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        try:
            connection = smtplib.SMTP('127.0.0.1', 1025)
            connection.starttls()
            connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        except Exception as e:
            if not self.fail_silently:
                raise e
        
