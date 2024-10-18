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

#@login_required
def update_keys(request):
    user = token_user(request)
    if user:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                print(data)
                
                print(f'Avant: {user.player1Up}')
                print(f'Avant: {user.player2Up}')

                moveUpP1 = data.get('moveUpP1')
                if moveUpP1:
                    user.player1Up = moveUpP1
                moveDownP1 = data.get('moveDownP1')
                if moveDownP1:
                    user.player1Down = moveDownP1
                moveUpP2 = data.get('moveUpP2')
                if moveUpP2:
                    user.player2Up = moveUpP2
                moveDownP2 = data.get('moveDownP2')
                if moveDownP2:
                    user.player2Down = moveDownP2
                pause = data.get('pause')
                if pause:
                    user.pause = pause
                mute = data.get('mute')
                if mute:
                    user.mute = mute
                user.save()

                print(f'Apres: {user.player1Up}')
                print(f'Apres: {user.player2Up}')

                return JsonResponse({'Message' : 'Key changed successfully'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid request body'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    return JsonResponse({'error': 'No user'}, status=405)

@login_required
def update_user(request):
    user = token_user(request)
    
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)

        print(user.username) 
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
        print(user.anonymized)
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
        return ''
    username, domain = email.split('@')
    masked_username = username[:2] + '****'
    return f"{masked_username}@{domain}"

def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def anonymize_data(user):
    user.email = mask_email(user.email)
    user.phone_number = mask_phone_number(user.phone_number)