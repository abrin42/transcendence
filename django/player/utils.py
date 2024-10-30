from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core import serializers
from django.core.serializers import serialize
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import JsonResponse

from .models import Player
from .jwt import token_user
import os
import requests
import json

def get_csrf_token(request):
    if request.COOKIES.get('csrftoken') is None:
        csrf_token = get_token(request)
    csrf_token = request.COOKIES.get('csrftoken')
    request.session['csrf'] = csrf_token

    response = JsonResponse({'message': 'CSRF token generated'}, status=200)
    response.set_cookie('csrftoken', csrf_token)
    return response

def verify_user(request):
    if request.method == 'GET':
        try:
            user = get_object_or_404(Player, username=request.user.username)
            player_data = serializers.serialize('json', [user])

            return JsonResponse({'player_data': player_data}, content_type='application/json', status=200)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

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

#############################################################

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
