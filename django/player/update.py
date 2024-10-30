from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .utils import get_csrf_token
from .jwt import generate_jwt, token_user, set_jwt_token

import json
import hashlib

@login_required
def update_language(request):
    user = token_user(request)
    if user:
        if request.method == "POST":
            if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
                return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
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
            if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
                return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
            try:
                data = json.loads(request.body)

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
        user.nickname = data.get('nickname', user.nickname)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.profile_picture = data.get('profile_picture', user.profile_picture)
        user.email_2fa_active = data.get('email_2fa_active', user.email_2fa_active)
        user.sms_2fa_active = data.get('sms_2fa_active', user.sms_2fa_active)
        user.anonymized = data.get('anonymized', user.anonymized)
        if user.anonymized:
            anonymize_data(user)
        password = data.get('password')
        if password:
            user.set_password(password)
            user.newpassword = None
            user.save()
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                authenticated_user.save()
                get_csrf_token(request)
                token = generate_jwt(authenticated_user)
                response = JsonResponse({
                    'redirect_url': '/dashboard/',
                    'message': 'Update successful!',
                }, status=200)
                set_jwt_token(response, token)
                return response
            return JsonResponse({'error': 'Échec de l\'authentification.'}, status=400)
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
    user.original_email = user.email
    user.original_phone_number = user.phone_number

    user.email = mask_email(user.email)
    user.phone_number = mask_phone_number(user.phone_number)