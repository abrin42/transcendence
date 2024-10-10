from django.shortcuts import render
from player.jwt import token_user
import json
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Game, BlacklistedToken
import asyncio
from player.models import Player 


def game(request):
    return render(request, 'game/game.html')

# @login_required
def creatgame(data):

    game = Game(
        player1 = data.player1,
        player2 = data.player2,
        socketp1 = data.socketp1,
        socketp2 = data.socketp2,
        scorep1 = 0,
        scorep2 = 0,
        state = "active",
    )
    game.save()

    return (JsonResponse({'message': 'gameIDInfo', 'gameID': game.id}, status=200))




#changer le thread de la balle pour pouvoir le meme pour les deux j


# j1 clique vers match meking
# j1 post pour remplir la bdd avec ses info 
# while qui check toutes les 0.5 seconde si j2 danbs bdd puis break pquand j2 pour rediriger 
# check si la derniere room a 2 jouer (non)

# j2 clique vers match meking
# j2 get pour remplir avec ses info
#  check si la derniere room a 2 jouer (oui)
#  creation de weebsocket 
#  redirection vers legacy/room
# 
