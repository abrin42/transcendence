from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import BlacklistedToken, Player
import jwt
import datetime

User = get_user_model()

def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt(token):
    if BlacklistedToken.objects.filter(token=token).exists():
        return {'error': 'Token is blacklisted'}
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        user = Player.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.DecodeError:
        return {'error': 'Token is invalid'}
    except Player.DoesNotExist:
        return {'error': 'User not found'}


def token_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        JsonResponse({'valid': False, 'message': 'No token found'}, status=401)
        return redirect('/player/login/')
    user = decode_jwt(token)
    if not user:
        JsonResponse({'valid': False, 'message': 'Invalid or expired token'}, status=401)
        return redirect('/player/login/')
    print(f"(token_user) {user}")
    return user


def set_jwt_token(response, token):
    response.set_cookie(
        'jwt',
        token,
        httponly=True,  # Prevent JavaScript access to the cookie
        secure=True,  # Use Secure flag to ensure it's only sent over HTTPS
        samesite='Lax'  # Prevent CSRF attacks
    )


def verify_jwt(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'valid': False, 'message': 'No token found'}, status=401)
    
    user = decode_jwt(token)
    if user:
        print(f"(verify_jwt)user: {user}")
        return JsonResponse({'valid': True, 'message': 'Token is valid'})
    else:
        return JsonResponse({'valid': False, 'message': 'Invalid or expired token'}, status=401)