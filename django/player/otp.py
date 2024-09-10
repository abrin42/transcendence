import pyotp
import vonage
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def send_otp(request, totp, contact, method):
    otp = totp.now()
    print("----------------------------------")
    print(f"Your one time password is {otp}")
    print("----------------------------------")

    if method == 'sms':
        client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_SECRET_KEY)
        sms = vonage.Sms(client)
        responseData = sms.send_message(
        {
            "from": "PONG WARS",
            "to": contact,
            "text": f"Your one time password is {otp}\n",
        })
        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    elif method == 'email':
        # SMTP Server Configuration and Email details
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD
        
        receiver_email = contact
        subject = "PONG Verification Code"
        body = f"Your Verification code is : {otp}"

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, receiver_email, msg.as_string())
                print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
        print("----------------------------------")

