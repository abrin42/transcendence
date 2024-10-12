from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Player
import os
import json
import requests
from django.contrib.auth.decorators import login_required


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
    player = verify_user(request)
    print(player)
    if player:
        player_data = serializers.serialize('json', [player])
    player_data = json.dumps({'error': 'User not found'})
    return JsonResponse({'player_data': player_data}, content_type='application/json')

@login_required
def verify_user(request):
    try:
        user = get_object_or_404(Player, username=request.user.username)
        player_data = serializers.serialize('json', [user])

        print(f"verify_user/username: {user.username}")
        print(f"verify_user/phone_number: {user.phone_number}")
        print(f"verify_user/email: {user.email}")

        return JsonResponse({'player_data': player_data}, content_type='application/json', status=200)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
