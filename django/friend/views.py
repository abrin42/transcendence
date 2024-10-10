from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
from .serialize import FriendSerializer
@login_required
def index(request):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    return render(request, "friend/index.html")

@login_required
def add(request):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    if request.method == 'POST':
        you = request.user
        you.last_login = timezone.now()
        you.save()
        if request.POST.get('username') == you.username:
            messages.add_message(request, messages.INFO, "can't add yourself")
            return render(request, "friend/add.html")
            #return JsonResponse({'error': "Can't add yourself"}, status=400)
        users = Player.objects.filter(username=request.POST.get('username'))
        if len(users) == 0:
            messages.add_message(request, messages.INFO, ("user doesn't exist"))
            return render(request, "friend/add.html")
            #return JsonResponse({'error': "user doesn't exist"}, status=400)
        new_friend = Friendship.objects.filter(Q(user=you, friend=users[0]) | Q(user=users[0], friend=you))
        if len(new_friend) != 0:
            messages.add_message(request, messages.INFO, ("invitation already sent"))
            return render(request, "friend/add.html")
            #return JsonResponse({'error': "invitation already sent"}, status=400)
        new_friend = Friendship(user=you, friend=users[0])
        new_friend.save()
        return render(request, "friend/work.html", {'friend':users[0], 'you':you}) #faire le changement vers les page front return JsonResponse({'redirect_url': '/......./'}, status=302)
        # Handle the submitted username as needed
        # For example, you can query the User model or process it in other ways
    return render(request, "friend/add.html")
    #return JsonResponse({'error': "Invalid request methode"}, status=405)

@login_required
def delete_friend(request, id_friendship):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    request = Friendship.objects.get(id=id_friendship)
    request.delete()
    return redirect("friend:list")

@login_required
def accept(request, id_friendship):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    request = Friendship.objects.get(id=id_friendship)
    request.status = 'accepted'
    request.save()
    return redirect("friend:pending")

@login_required
def refuse(request, id_friendship):
    user = token_user(request)
    if user is None: 
        return redirect(reverse('player:login'))
    request = Friendship.objects.get(id=id_friendship)
    request.status = 'refused'
    request.save()
    return redirect("friend:pending")

@login_required
def list(request):
    you = token_user(request)
    friends = Friendship.objects.filter(Q(user=you, status='accepted') | Q(friend=you, status='accepted'))
    you.last_login = timezone.now()
    you.save()
    #return render(request, "friend/list.html", {'friends':friends, 'you':you})
    #data = serializers.serialize('json', friends, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    serializer = FriendSerializer(friends)
    return JsonResponse(serializer.data, safe=False) 
    #return HttpResponse(friend_list, content_type='application/json')

@login_required
def pending(request):
    you = token_user(request)
    friends = Friendship.objects.filter(Q(friend=you, status='pending'))
    you.last_login = timezone.now()
    you.save()
    return render(request, "friend/pending.html", {'friends':friends, 'you':you})
    #data = serializers.serialize('json', friends)
    #return HttpResponse(data, content_type='application/json')

@login_required
def refused(request):
    you = token_user(request)
    friends = Friendship.objects.filter(Q(friend=you, status='refused'))
    you.last_login = timezone.now()
    you.save()
    #return render(request, "friend/refused.html", {'friends':friends, 'you':you})
    data = serializers.serialize('json', friends, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')