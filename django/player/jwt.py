from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import now
from .models import BlacklistedToken, Player
import jwt
import datetime

def update_user_zero():
    ano = Player.objects.filter(username='anonymous', email='cyberpong16@gmail.com')
    if len(ano) != 1:
        ano = Player(username='anonymous', email='cyberpong16@gmail.com',nickname="anonymous",rank=0)
        ano.save()

def generate_jwt(user):
    update_user_zero()
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt(token):
    if BlacklistedToken.objects.filter(token=token).exists():
        return None
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        user = Player.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
    except Player.DoesNotExist:
        return None

def token_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return None
    user = decode_jwt(token)
    if not user or user is None:
        return None
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
        return JsonResponse({'valid': False, 'message': 'No token found', 'user': None}, status=401)
    user = decode_jwt(token)
    if isinstance(user, Player):
        return JsonResponse({'valid': True, 'message': 'Token is valid', 'user': user}, content_type='application/json')
    return JsonResponse({'valid': False, 'message': 'Invalid or expired token', 'user': None}, status=401)