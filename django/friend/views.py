from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse
from .models import Friendship, Player
from player.jwt import token_user
import json
from django.core import serializers
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from datetime import datetime, timedelta
from .serialize import FriendshipSerializer
from django.views.decorators.csrf import csrf_exempt

def index(request):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    return render(request, "friend/index.html")

def add(request):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        if username == user.username:
            return JsonResponse({'error': "Can't add userrself"}, status=401)
        users = Player.objects.filter(username=username)
        new_friend = Friendship.objects.filter(Q(user=user, friend=users[0]) | Q(user=users[0], friend=user))
        if len(new_friend) != 0:
            return JsonResponse({'error': "invitation already sent"}, status=400)
        new_friend = Friendship(user=user, friend=users[0])
        new_friend.save()
        return JsonResponse({'redirect_url': '/'}, status=200)
    return JsonResponse({'error': "Invalid request methode"}, status=405)

def delete(request):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    data = json.loads(request.body)
    username = data.get('username')
    other = Player.objects.filter(username=username)
    request = Friendship.objects.filter(Q(user=user, friend=other[0]) | Q(user=other[0], friend=user))
    request.delete()
    #return redirect("friend:list")
    return JsonResponse({'redirect_url': '/'}, status=200)

def help(request):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        users = Player.objects.filter(username=username)
        if len(users) == 0:
            return JsonResponse({'error': "user doesn't exist"}, status=400)
        new_friend = Friendship.objects.filter(user=users[0], friend=user)
        for elem in new_friend:
            elem.status = 'accepted'
            elem.save()
        return JsonResponse({'redirect_url': '/'}, status=200)
    return JsonResponse({'error': "Invalid request methode"}, status=405)

def refuse(request, id_friendship):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    request = Friendship.objects.get(id=id_friendship)
    request.status = 'refused'
    request.save()
    return redirect("friend:pending")

def list(request):
    you = token_user(request)
    friends = Friendship.objects.filter(Q(user=you, status='accepted') | Q(friend=you, status='accepted'))

    #return render(request, "friend/list.html", {'friends':friends, 'you':you})
    data = serializers.serialize('json', friends, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(data, safe=False, content_type='application/json')
    

def pending(request):
    you = token_user(request)
    friends = Friendship.objects.filter(Q(friend=you, status='pending'))
    you.last_login = timezone.now()
    you.save()
    #return render(request, "friend/pending.html", {'friends':friends, 'you':you})
    data = serializers.serialize('json', friends, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(data, safe=False, content_type='application/json')

def refused(request):
    you = token_user(request)
    friends = Friendship.objects.filter(Q(friend=you, status='refused'))
    you.last_login = timezone.now()
    you.save()
    #return render(request, "friend/refused.html", {'friends':friends, 'you':you})
    data = serializers.serialize('json', friends, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(data, safe=False, content_type='application/json')
    #return HttpResponse(data, content_type='application/json')