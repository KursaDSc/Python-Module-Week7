import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")


def send_email_to(to_email, subject, body):
    # SMTP ayarlarını kendi mail servisiniz için doldurun
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.getenv("SENDER_EMAIL")
    smtp_pass = os.getenv("SENDER_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_email], msg.as_string())