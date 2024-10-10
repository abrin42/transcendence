from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
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
from django.core import serializers

#@login_required
def update_language(request):
    user = token_user(request)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            language = data.get('language')
            user.language = language
            user.save()
            response = JsonResponse({'redirect_url': '/dashboard/'}, status=302)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_nickname(request):
    user = token_user(request)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nickname = data.get('nickname')
            user.nickname = nickname
            user.save()
            response = JsonResponse({'redirect_url': '/dashboard/'}, status=302)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_email(request):
    user = token_user(request)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            user.email = email
            user.save()
            response = JsonResponse({'redirect_url': '/dashboard/'}, status=302)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_phone_number(request):
    user = token_user(request)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            user.phone_number = phone_number
            user.save()
            response = JsonResponse({'redirect_url': '/dashboard/'}, status=302)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_profile_picture(request):
    user = token_user(request)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            profile_picture = data.get('profile_picture')
            user.profile_picture = profile_picture
            user.save()
            response = JsonResponse({'redirect_url': '/dashboard/'}, status=302)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
