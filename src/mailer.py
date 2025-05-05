from email.utils import formataddr
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import *

def send_email(to_email, subject, body):
    message = MIMEMultipart()
    message["From"] = formataddr((MAIL_FROM, MAIL_EMAIL))
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    server = SMTP(MAIL_HOST, MAIL_PORT)
    server.starttls()
    server.login(MAIL_EMAIL, MAIL_PASSWORD)
    server.sendmail(MAIL_EMAIL, to_email, message.as_string())
