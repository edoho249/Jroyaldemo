# python imports
import os
import ssl
import smtplib
from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# installed imports
from flask import url_for, render_template

# local imports
from app import logger
from app.modules.verification import generate_confirmation_token


def send_email(receiver_email, subject, plaintext, html=None):
    # Connection configuration
    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    PORT = 465  # For starttls
    USERNAME = os.environ.get("SENDER_EMAIL")
    PASSWORD = os.environ.get("PASSWORD")

    # Message setup
    message = MIMEMultipart()
    message["Subject"] = Header(subject)
    message["From"] = Header(f"{os.environ.get('SENDER_NAME')}")
    message["To"] = Header(receiver_email)

    # Turn text into plain or HTML MIMEText objects
    part1 = MIMEText(plaintext, "plain")
    if html:
        part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    if html:
        message.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()

    success = False  # Initialize success variable

    # Try to log in to server and send email
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, receiver_email, message.as_string())
            success = True  # Set success to True on successful send
    except Exception as e:
        # Print error messages to stdout
        logger.error(e)
    finally:
        return success  # Return success value


# Convenience function - registration / verification email
def send_registration_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for(
        "auth.confirm_email", token=token, _external=True, _scheme="https"
    )
    logger.info(f"Generated confirm URL: {confirm_url}")
    # check if user already registered
    if (datetime.utcnow() - user.created_at) > timedelta(
        minutes=1
    ):  # user account is over a minute
        subject = "Confirm changes - Please verify the changes made to your account."
        plaintext = "Re-verify your email address."
        html = render_template(
            "verify_changes.html", confirm_url=confirm_url, user=user
        )
    else:
        subject = "Registration successful - Please verify your email address."
        plaintext = f"Welcome {user.display_name()}. Please follow the link provided to verify your email."
        html = render_template(
            "verification_email.html", confirm_url=confirm_url, user=user
        )
    return send_email(user.email, subject, plaintext, html)


# Convenience function - forgot password email
def send_forgot_password_email(user):
    token = generate_confirmation_token(user.email)
    change_url = url_for(
        "auth.change_password", token=token, _external=True, _scheme="https"
    )
    subject = "Change password - Follow the link below to change your password."
    plaintext = "Follow the link to change your password."
    html = render_template("change_password.html", change_url=change_url, user=user)

    return send_email(user.email, subject, plaintext, html)
