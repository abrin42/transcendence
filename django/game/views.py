from django.shortcuts import render, get_object_or_404
from player.jwt import token_user
import json
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Game
from player.models import Player 
from django.core import serializers
import asyncio
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


def creat_game_local(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username1 = data.get('username1')
            username2 = data.get('username2')
            print("----username----")
            print(username1)
            print(username2)
            player1 = get_object_or_404(Player, username=username1)
            player2 = get_object_or_404(Player, username=username2)
            print("----obj player----")
            print(player1)
            print(player2)
            latest_game = Game.objects.create(state='waiting', player1=player1, scorep1=0, player2=player2, scorep2=0)
            print("----obj game----")
            print(latest_game)

            serializer = GameSerializer(latest_game)
            data = serializer.data
            print("----serializer date ----")
            print(data)
            return JsonResponse(data, safe=False, content_type='application/json')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

        
def insertPlayer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')

            player = get_object_or_404(Player, username=username)
            latest_game = Game.objects.order_by('-id').first()

            if latest_game is None:
                latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
            elif latest_game.player1 != player and (latest_game.player2 is None or latest_game.player2 != player):
                if latest_game.player2 is not None:
                    latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
                else:
                    latest_game.player2 = player
                    latest_game.state = 'active'  # Vous pouvez également changer l'état si nécessaire
                    latest_game.scorep2 = 0
                    latest_game.save()

            data = serializers.serialize('json', [latest_game])
            return JsonResponse(data, safe=False, content_type='application/json')

            #serializer = GameSerializer(latest_game)
            #serializer_data = json.loads(serialize('json', [serializer]))[0]['fields']
            #return JsonResponse(serializer_data, safe=False) 
            # return HttpResponse(data,content_type='application/json')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

#@login_required
def update_game(request):
    if request.method == "POST":
        try:
            # game = Game.objects.order_by('-id').first()
            data = json.loads(request.body)
            id = data.get('id')
            game = get_object_or_404(Game, id=id)
            if not game:
                return JsonResponse({'error': 'No game found to update.'}, status=404)

            #game_id = data.get('gameID')
            #print(game_id)
            #game = get_object_or_404(Game, id=game_id)
            
            game.mode = data.get('mode')
            game.scorep1 = data.get('scorep1')
            game.scorep2 = data.get('scorep2')
            game.save()

            print(game.scorep1)
            print(game.scorep2)
            print(game.mode)
            print(game.player1)
            print(game.player2)
            
            return JsonResponse({'message': 'Registration successful'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



#changer le thread de la balle pour pouvoir le meme pour les deux 

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
