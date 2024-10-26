from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .otp import create_otp
from .jwt import generate_jwt, token_user, set_jwt_token
from .models import Player, BlacklistedToken
from .utils import set_picture_42, get_csrf_token
from datetime import datetime
import pyotp
import requests
import json
from collections import deque
import asyncio
from django.middleware.csrf import get_token

matchmaking = deque()

def register_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = f"_{data.get('username')}"
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password1')
            
            print(username)
            print(password)
            
            if Player.objects.filter(username=username).exists():
                return JsonResponse(
                    {'error': 'Le nom d\'utilisateur existe déjà.'}, status=400
                )

            user, created = Player.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            user.email = email
            user.phone_number = phone_number
            user.set_password(password)
            user.save()
            print(user.username)
            print(user.password)
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user:
                set_user_keys(user)
            
                login(request, authenticated_user)
                authenticated_user.nickname = user.username[1:] 
                authenticated_user.save()
                get_csrf_token(request)

                token = generate_jwt(authenticated_user)
                response = JsonResponse({
                    'message': 'Inscription réussie!',
                    'redirect_url': '/dashboard'
                }, status=200)
                set_jwt_token(response, token)
                return response

            return JsonResponse({'error': 'Échec de l\'authentification.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Corps de la requête invalide.'}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

def set_user_keys(user):
    user.player1Up = 'KeyW'
    user.player1Down = 'KeyS'
    user.player2Up = 'ArrowUp'
    user.player2Down = 'ArrowDown'
    user.pause = 'KeyP'
    user.mute = 'KeyM'
    user.save()

def login_view(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        username = f"_{data.get('username')}"
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        player = get_object_or_404(Player, username=username)
        if not check_password(password, player.password):
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
        
        print(f'username: {player.username}, email_2fa_active: {player.email_2fa_active}')
        login(request, player)
        get_csrf_token(request)
        print("-----------------------------------------------------------------")
        print(f"/login/request.session['csrf']: {request.session.get('csrf')}")     
        print(f"/login/request.COOKIES.get('csrftoken'): {request.COOKIES.get('csrftoken')}")    
        print("-----------------------------------------------------------------")

        if not player.email_2fa_active and not player.sms_2fa_active:
            token = generate_jwt(player)

            if not player.nickname:
                player.nickname = player.username[1:]
                player.save()

            response = JsonResponse({
                'message': 'Login successful',
                'redirect_url': '/'
            }, status=200)

            set_jwt_token(response, token)
            return response

        player_data = serializers.serialize('json', [player])
        return JsonResponse({
            'player_data': player_data,
            'redirect_url': '/2fa/'
        }, content_type='application/json')

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request body'}, status=400)


@login_required
def tfa_view(request):
    if request.method == "POST":
        get_csrf_token(request)
        print("-----------------------------------------------------------------")
        print(f"/tfa/request.session['csrf']: {request.session.get('csrf')}")     
        print(f"/tfa/request.COOKIES.get('csrftoken'): {request.COOKIES.get('csrftoken')}")    
        print("-----------------------------------------------------------------")
        if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
            return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
        
        try:
            user = get_object_or_404(Player, username=request.user.username)
            print(f"2fa user: {user}")
            create_otp(request, user)
            return JsonResponse({'message': 'Code sent successfully', 'redirect_url': '/2fa/'}, status=200)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def otp_view(request):
    ########################### Here I use the user from request and call its Player object. I apply the JWT token only when the 2FA/OTP is valid
    try:
        user = get_object_or_404(Player, username=request.user.username)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    ###########################
    if request.method == "POST":
        if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
            return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
        try:
            data = json.loads(request.body)
            user_otp = data.get('user_otp')
            otp_secret_key = request.session.get('otp_secret_key')
            otp_valid_date = request.session.get('otp_valid_date')
         
            print(f'user_otp: {user_otp}')
            print(f'otp_secret_key: {otp_secret_key}')
            print(f'otp_valid_date: {otp_valid_date}')

            if otp_secret_key and otp_valid_date:
                valid_until = datetime.fromisoformat(otp_valid_date)
                print(f'valid_until: {valid_until}')

                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    print(f'totp: {totp}')

                    if totp.verify(user_otp):
                        token = generate_jwt(user)
                        print(f'token: {token}')

                        response = JsonResponse({'redirect_url': '/2fa'}, status=302)

                        csrf_token = get_token(request)
                        user.csrf = csrf_token

                        set_jwt_token(response, token)                        
                        print("JWT OK")
                        
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        del request.session['username']
                        del request.session['otp_method']

                        return response
                    
                    return JsonResponse({'error': 'Invalid OTP'}, status=400)
                return JsonResponse({'error': 'Your OTP code has expired'}, status=400)
            
            return JsonResponse({'error': 'No OTP session found. Please request a new code.'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def login42_view(request):
    if request.method == "POST":
        oauth_url = f"{settings.FT42_OAUTH_URL}?client_id={settings.FT42_CLIENT_ID}&redirect_uri={settings.FT42_REDIRECT_URI}&response_type=code"
        return JsonResponse({'url': oauth_url}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def auth_42_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('/log/')

    token_url = 'https://api.intra.42.fr/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.FT42_CLIENT_ID,
        'client_secret': settings.FT42_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.FT42_REDIRECT_URI,
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200: #if the HTTP request (get) is not successful 
        return redirect('/log/')

    token_info = response.json()
    access_token = token_info.get('access_token')
    if not access_token:
        return redirect('/log/')

    user_info_response = requests.get(
        'https://api.intra.42.fr/v2/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if user_info_response.status_code != 200: #if the HTTP request (get) is not successful 
        return redirect('/log/')

    user_info = user_info_response.json()
    login_name = user_info.get('login')
    username = f'{login_name}'
    email = user_info.get('email')
    profile_picture = user_info["image"]["versions"]["small"]

    if not username:
        return redirect('/log/')

    user, created = Player.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    
    if user is not None:
        user.student = True
        if user.nickname is None:
            user.nickname = user.username
        if profile_picture and user.profile_picture is None: 
            user.profile_picture = profile_picture
        user.save()
        login(request, user)
        get_csrf_token(request)

        token = generate_jwt(user)
        response = redirect('/')
        set_jwt_token(response, token)
        return response
    return redirect('/log/')

@login_required
def logout_view(request):
    if request.method == "POST":
        if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
            return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
        token = request.COOKIES.get('jwt')
        print(token)
        response = redirect('/log')
        if token:
            BlacklistedToken.objects.create(token=token)
            response.delete_cookie('jwt')
        logout(request)
        return response
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def delete_p(request):
    user = token_user(request)
    user.delete()

@login_required
def delete_account(request):
    user = token_user(request)
    user.delete()
    return JsonResponse({'redirect_url': '/log'}, status=200)

def connected_user(request):
    if request.method == 'GET':
        try:
            user = token_user(request)
            if user is not None:
                user_data = json.loads(serialize('json', [user]))[0]['fields']
                return JsonResponse(user_data, safe=True, content_type='application/json') 
            return JsonResponse({'msg': 'User not found'}, status=204)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all_user(request):
    data = Player.objects.all().order_by("-rank")
    data = serializers.serialize('json', data)
    return JsonResponse(data, safe=False) 





def enter_matchmaking(request):
    user = token_user(request)
    if user in matchmaking:
        return JsonResponse({'error': 'Already in matchmaking'}, status=403)
    matchmaking.append(user)
    return JsonResponse({'redirect_url': '/matchmaking'}, status=302) #dans matchmaking il faut fetch get get_match

def quit_matchmaking(request):
    user = token_user(request)
    if user not in matchmaking:
        return JsonResponse({'error': 'Already left matchmaking'}, status=403)
    matchmaking.remove(user)
    return JsonResponse({'redirect_url': '/'}, status=302)

async def get_match(request):
    if len(matchmaking) >= 2:
        data = matchmaking[0]
        data.append(matchmaking[1])
        data = serializers.serialize('json', data)
        return JsonResponse(data, safe=False, content_type='application/json')

    await asyncio.sleep(0.5)
    return JsonResponse({'redirect_url': '/matchmaking'}, status=302)