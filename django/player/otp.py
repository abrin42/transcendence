import pyotp
import vonage
import smtplib
import json
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.core.mail import send_mail

def create_otp(request, user):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    
    request.session['username'] = user.username
    request.session['otp_secret_key'] = totp.secret
    request.session['otp_valid_date'] = (datetime.now() + timedelta(minutes=2)).isoformat()
    
    data = json.loads(request.body)
    otp_method = data.get('otp_method')
    if otp_method:
        print("POST otp_method")
        request.session['otp_method'] = otp_method  
    
    if  otp_method == 'sms':
        contact = str(user.phone_number)
        send_otp(request, totp, contact, method='sms')
    elif otp_method == 'email':
        contact = user.email
        send_otp(request, totp, contact, method='email')


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
        subject = 'CYBER PONG Verification'
        message = f"Your Verification code is : {otp}"
        send_mail(subject, message, 'cyberpong16@gmail.com', [contact])

