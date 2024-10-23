from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core import serializers
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .models import Player
from .jwt import token_user
import os
import requests

def verify_csrf(request):
    user = token_user(request)
    if not user.csrf:
        return False
    
    csrf_session = request.session.get('csrf_token')
    #print(f"/verify_csrf/csrf_session: {csrf_session}")

    if user.csrf != csrf_session:
        return False
    return True

def get_csrf_token(request):
    print(request)
    if request.method == 'GET':
        csrf_token = get_token(request)

        if not request.session.get('csrf_token'):
            print(f"/get_csrf_token/csrf_token: {csrf_token}")
            request.session['csrf_token'] = csrf_token
            response = JsonResponse({'message': 'CSRF token generated'}, status=200)
            response.set_cookie('csrftoken', csrf_token)
            return response
        
        user = token_user(request)
        if user:
            user.csrf = csrf_token
        response = JsonResponse({'message': 'CSRF token generated'}, status=200)
        response.set_cookie('csrftoken', csrf_token)
        return response
        #return JsonResponse({'error': 'Invalid request la'}, status=400)
    return JsonResponse({'error': 'Invalid request la'}, status=400)

def username_underscore(request):
    post_data = request.POST.copy()
    raw_username = post_data.get('username')
    if raw_username:
        post_data['username'] = f"_{raw_username}"
    return post_data
    
def set_picture_42(request, user, profile_picture):
    response = requests.get(profile_picture)
    if response.status_code == 200: #if the HTTP request (get) is successful 
        picture_name = f"{user.username}_profile.jpg"
        profile_pic_dir = os.path.join(settings.MEDIA_ROOT, "profile_pictures", user.username)

        if not os.path.exists(profile_pic_dir):
            os.makedirs(profile_pic_dir)
            user.profile_picture.save(picture_name, ContentFile(response.content), save=True)
    else:
        print(f"Failed to fetch profile picture, status code: {response.status_code}")

def verify_user(request):
    if request.method == 'POST':
        try:
            user = get_object_or_404(Player, username=request.user.username)
            player_data = serializers.serialize('json', [user])

            print(f"verify_user/username: {user.username}")
            print(f"verify_user/phone_number: {user.phone_number}")
            print(f"verify_user/email: {user.email}")

            return JsonResponse({'player_data': player_data}, content_type='application/json', status=200)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request la'}, status=400)

