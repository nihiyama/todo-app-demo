from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
import re

from app.utils.config import settings

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
email_template_dir = Path(__file__).resolve().parent / "email_templates"


def is_valid_email_address(email_address: str) -> bool:
    if email_regex.fullmatch(email_address):
        return True
    else:
        return False


def create_signup_mail_content(user_name: str, url: str) -> str:
    message_content = ""
    template = email_template_dir / "signup_content.txt"
    with open(template, "r") as f:
        content = f.read()
        content = content.replace("{{user_name}}", user_name)
        content = content.replace("{{url}}", url)
        message_content += content
    
    return message_content


def create_signup_mail_subject() -> str:
    message_subject = ""
    template = email_template_dir / "signup_subject.txt"
    with open(template, "r") as f:
        subject = f.read()
        message_subject += subject
    
    return message_subject


def send_mail(
    content: str,
    subject: str,
    email_to: List[str],
    email_cc: List[str] = [],
    email_bcc: List[str] = []
) -> bool:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr((settings.EMAIL_SENDER_NAME, settings.EMAIL_SENDER_ADDRESS))
    message["To"] = ",".join(email_to)
    if len(email_cc) > 0:
        message["Cc"] = ",".join(email_cc)
    if len(email_bcc) > 0:
        message["Bcc"] = ",".join(email_bcc)
    
    body = MIMEText(content, "plain")
    message.attach(body)

    try:
        with smtplib.SMTP(host=settings.EMAIL_SERVER_HOST, port=settings.EMAIL_SERVER_PORT) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
            s.send_message(message)
    except Exception:
        return False

    return True


def send_dummy_mail(
    content: str,
    subject: str,
    email_to: List[str],
    email_cc: List[str] = [],
    email_bcc: List[str] = []
) -> bool:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr((settings.EMAIL_SENDER_NAME, settings.EMAIL_SENDER_ADDRESS))
    message["To"] = ",".join(email_to)
    if len(email_cc) > 0:
        message["Cc"] = ",".join(email_cc)
    if len(email_bcc) > 0:
        message["Bcc"] = ",".join(email_bcc)
    
    body = MIMEText(content, "plain")
    message.attach(body)

    return True
