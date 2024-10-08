from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Player
import os
import json
import requests

def username_underscore(request):
    post_data = request.POST.copy()
    raw_username = post_data.get('username')
    if raw_username:
        post_data['username'] = f"_{raw_username}"
    return post_data
    
    return user

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

def is_auth(request):
    if not request.user.is_authenticated:
        return JsonResponse({'valid': False, 'message': 'No token found'}, status=401)
    user = get_object_or_404(Player, username=request.user.username)
    if not user:
        return JsonResponse({'valid': True, 'message': 'Token is valid', 'user': user_data}, content_type='application/json')
    return JsonResponse({'valid': False, 'message': 'Invalid or expired token'}, status=401)


def verify_user(request):
    if not request.user.is_authenticated:
        return redirect('/api/player/login/')
    try:
        user = get_object_or_404(Player, username=request.user.username)
    except Player.DoesNotExist:
        return redirect('/api/player/login/')

    print(f"username: {user.username}")
    print(f"phone_number: {user.phone_number}")
    return user