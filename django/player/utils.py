from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core import serializers
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .models import Player
import os
import requests

<<<<<<< HEAD
=======
def get_csrf_token(request):
    print(request)
    print(f"/getcsrf/request.session['csrf']: {request.session.get('csrf')}")     
    print(f"/getcsrf/request.COOKIES.get('csrftoken'): {request.COOKIES.get('csrftoken')}")     

    if request.COOKIES.get('csrftoken') is None:
        csrf_token = get_token(request)

    csrf_token = request.COOKIES.get('csrftoken')
    print(f"callback/ csrf_token: {csrf_token}")     
    request.session['csrf'] = csrf_token
    print(f"callback/ request.session.get['csrf']: {request.session.get('csrf')}")     
    
    response = JsonResponse({'message': 'CSRF token generated'}, status=200)
    response.set_cookie('csrftoken', csrf_token)
    return response
>>>>>>> b9eae8a8cbe6a91c7ef07eaa3b497e85d67695ac

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
