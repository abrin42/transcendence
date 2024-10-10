from django.shortcuts import render, get_object_or_404
from player.jwt import token_user
import json
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Game
import asyncio
from player.models import Player 
from django.core import serializers
from .serializers import GameSerializer

def game(request):
    return render(request, 'game/game.html')

# # @login_required
# def creatgame(data):

#     game = Game(
#         player1 = data.player1,
#         player2 = data.player2,
#         socketp1 = data.socketp1,
#         socketp2 = data.socketp2,
#         scorep1 = 0,
#         scorep2 = 0,
#         state = "active",
#     )
#     game.save()

#     return (JsonResponse({'message': 'gameIDInfo', 'gameID': game.id}, status=200))


def insertPlayer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')

            player = get_object_or_404(Player, username=username)

            latest_game = Game.objects.order_by('-id').first()
            if latest_game is None:
                latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
            elif latest_game.player2 is not None:
                latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
            else:
                latest_game.player2 = player
                latest_game.state = 'active'  # Vous pouvez également changer l'état si nécessaire
                latest_game.scorep2 = 0
                latest_game.save()

            serializer = GameSerializer(latest_game)
            return JsonResponse(serializer.data, safe=False) 
            # return HttpResponse(data,content_type='application/json')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


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
