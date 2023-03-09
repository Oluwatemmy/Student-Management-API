from flask_sqlalchemy import SQLAlchemy
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = SQLAlchemy()

def generate_reset_token(length):
    return secrets.token_hex(length)

def generate_random_string(length):
    """
    Generate a random string of alphanumeric characters of given length
    """
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

def send_email(user_mail, token):
    """
    Sends a password reset email to the specified email address.
    """
    sender_email = "temmyghold00@gmail.com"
    password = "iceksvttjftmlwat"
    subject = "Password Reset Request"
    message = f""" 
    Hi {user_mail.name},
    You requested for a password reset. Click on the link below to reset your password.
    http://localhost:5000/auth/password-reset/{token}
    If you did not make this request, please ignore this email.
    Regards,
    Team
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_mail.email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, user_mail.email, text)
    server.quit()
