from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .otp import send_otp, create_otp
from .jwt import generate_jwt, decode_jwt, token_user, set_jwt_token
from .forms import RegisterForm, ChangePasswordForm, UpdateForm
from .models import Player, BlacklistedToken
from .utils import set_picture_42, username_underscore, verify_user
from datetime import datetime, timedelta
import os
import pyotp
import requests
import jwt
import json
import logging
import hashlib

@login_required
def update_language(request):
    user = token_user(request)
    if user:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                language = data.get('language')
                if language:
                    user.language = language
                    user.save()
                response = JsonResponse({'redirect_url': '/dashboard/'}, status=302)
                return response
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid request body'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    return JsonResponse({'error': 'No user'}, status=405)

@login_required
def update_keys(request):
    user = token_user(request)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            print(f'Avant: {user.moveUpP1}')
            user.moveUpP1 = data.get('moveUpP1')
            user.moveDownP1 = data.get('moveDownP1')
            user.moveUpP2 = data.get('moveUpP2')
            user.moveDownP2 = data.get('moveDownP2')
            user.pause = data.get('pause')
            user.mute = data.get('mute')
            user.save()
            print(f'Apres: {user.moveUpP1}')
            return JsonResponse({'Message' : 'Key changed successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_user(request):
    user = token_user(request)  # Ensure this function is implemented correctly.
    
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)

        print(user.username)  # For debugging, consider logging instead.
        user.nickname = data.get('nickname', user.nickname)
        user.email = data.get('email', user.email)
        
        password = data.get('password')
        if password:
            user.password = password

        user.phone_number = data.get('phone_number', user.phone_number)
        user.profile_picture = data.get('profile_picture', user.profile_picture)
        user.email_2fa_active = data.get('email_2fa_active', user.email_2fa_active)
        user.sms_2fa_active = data.get('sms_2fa_active', user.sms_2fa_active)
        user.anonymized = data.get('anonymized', user.anonymized)
        print(user.anonymized)  # For debugging.
        if user.anonymized:
            anonymize_data(user)

        user.save()
        return JsonResponse({'redirect_url': '/dashboard/'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request body'}, status=400)

#####################################################
#                   ANONYMIZATION                   #
#####################################################

def mask_phone_number(phone):
    phone_str = str(phone)  
    if len(phone_str) < 4:
        return phone_str
    return phone_str[:2] + '****' + phone_str[-2:]

def mask_email(email):
    if not email or '@' not in email:
        return ''  # Handle invalid email formats.
    username, domain = email.split('@')
    masked_username = username[:2] + '****'
    return f"{masked_username}@{domain}"

def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def anonymize_data(user):
    """Anonymize the user's phone number and email."""
    user.email = mask_email(user.email)
    user.phone_number = mask_phone_number(user.phone_number)