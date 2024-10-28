from django.shortcuts import render, get_object_or_404
from player.jwt import token_user
import json
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Game
from player.models import Player 
from django.core import serializers
import asyncio
from .serializers import GameSerializer
from .serializers import PlayerSerializer
from django.core.serializers import serialize


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

def get_all_games(request):
    if request.method == 'GET':
        data = Game.objects.all().order_by("-created_at")
        data = serializers.serialize('json', data, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def setGameRank(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            game = get_object_or_404(Game, id=id)

            print("-------------------------fetch set rank-------------------------")
            print("score p1")
            print(game.scorep1)
            print("score p2")
            print(game.scorep2)
            game.state = 'end'
            game.save()

            if game.scorep1 == 5:
                print("p1 win")
                game.player1.win += 1
                game.player2.lose += 1
                newRank = (game.scorep1 - game.scorep2) * 10
                game.player1.rank += newRank
                game.player2.rank -= (newRank / 2)
            elif game.scorep2 == 5:
                print("p2 win")
                game.player2.win += 1
                game.player1.lose += 1
                newRank = (game.scorep2 - game.scorep1) * 10
                game.player2.rank += newRank
                game.player1.rank -= (newRank / 2)
            game.player1.save()
            game.player2.save()
            print("-------------------------end fetch set rank-------------------------")
            return JsonResponse({'message': 'Registration successful'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def getGameInfo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_id = data.get('id')
            game = get_object_or_404(Game, id=game_id)

            serializer = GameSerializer(game)
            data = serializer.data
            return JsonResponse(data, safe=False, content_type='application/json')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def createOneFalsePlayer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = f"#{data.get('username1')}"
            print(username)

            player1, created = Player.objects.get_or_create(
                username=username,
                defaults={'username':username}
            )
            print(player1.username)

            user = json.loads(serialize('json', [player1]))[0]['fields']
            return JsonResponse(user, safe=True, content_type='application/json') 
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def createFalsePlayer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user1 = f"#{data.get('username1')}"
            user2 = f"#{data.get('username2')}"
            user3 = f"#{data.get('username3')}"
            user4 = f"#{data.get('username4')}"

            player1, created = Player.objects.get_or_create(
                username=user1,
                defaults={'username': user1}
            )
            player2, created = Player.objects.get_or_create(
                username=user2,
                defaults={'username': user2}
            )
            player3, created = Player.objects.get_or_create(
                username=user3,
                defaults={'username': user3}
            )
            player4, created = Player.objects.get_or_create(
                username=user4,
                defaults={'username': user4}
            )
            players = [player1, player2, player3, player4]
            serialized_players = PlayerSerializer(players, many=True)            
            
            return JsonResponse({'players': serialized_players.data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def create_game_local(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username1 = data.get('username1')
            username2 = data.get('username2')
            player1 = get_object_or_404(Player, username=username1)
            player2 = get_object_or_404(Player, username=username2)
            latest_game = Game.objects.create(state='waiting', player1=player1, scorep1=0, player2=player2, scorep2=0)
            print("////////////////////////////////")
            print(f"latest_game.id: {latest_game.id}")
            print("////////////////////////////////")
            serializer = GameSerializer(latest_game)
            data = serializer.data
            return JsonResponse(data, safe=False, content_type='application/json')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

        
# def insertPlayer(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')

#             player = get_object_or_404(Player, username=username)
#             latest_game = Game.objects.order_by('-id').first()
#             # if game state est != wating cree une nouvelle game 
#             if latest_game.mode == 'waiting':
#                 # if latest_game is None or latest_game.player2 is not None and latest_game.player1 != player:
#                     # latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
#                 if latest_game.player1 != player:
#                     latest_game.player2 = player
#                     latest_game.state = 'active'
#                     latest_game.scorep2 = 0
#                     latest_game.save()
#                 serializer = GameSerializer(latest_game)
#                 data = serializer.data
#                 return JsonResponse(data, safe=False, content_type='application/json')
                
#             elif latest_game.player1 != player:
#                 latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)

#             serializer = GameSerializer(latest_game)
#             data = serializer.data
#             return JsonResponse(data, safe=False, content_type='application/json')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid request body'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

def insertPlayer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            print("---- before player ----")
            player = get_object_or_404(Player, username=username)
            print("---- after player ----")
            latest_game = Game.objects.order_by('-id').first()
            if latest_game is None:
                latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
                serializer = GameSerializer(latest_game)
                data = serializer.data
                return JsonResponse(data, safe=False, content_type='application/json')
            if latest_game.state == 'waiting':
                if latest_game.player1 != player and latest_game.player2 is None:
                    latest_game.player2 = player
                    latest_game.scorep2 = 0
                    latest_game.save()
                serializer = GameSerializer(latest_game)
                data = serializer.data
                return JsonResponse(data, safe=False, content_type='application/json')
                
            elif latest_game.state != 'waiting':
                latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
            serializer = GameSerializer(latest_game)
            data = serializer.data
            return JsonResponse(data, safe=False, content_type='application/json')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# def insertPlayer(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')

#             player = get_object_or_404(Player, username=username)
#             latest_game = Game.objects.order_by('-id').first()

#             if latest_game is None:
#                 latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
#             elif latest_game.player1 != player and (latest_game.player2 is None or latest_game.player2 != player):
#                 if latest_game.player2 is not None:
#                     latest_game = Game.objects.create(state='waiting', player1=player, scorep1=0)
#                 else:
#                     latest_game.player2 = player
#                     latest_game.state = 'active'  # Vous pouvez également changer l'état si nécessaire
#                     latest_game.scorep2 = 0
#                     latest_game.save()

#             # data = serializers.serialize('json', [latest_game])
#             # return JsonResponse(data, safe=False, content_type='application/json')


#             serializer = GameSerializer(latest_game)
#             data = serializer.data
#             return JsonResponse(data, safe=False, content_type='application/json')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid request body'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

#@login_required
def update_game(request):
    if request.method == "POST":
        
        if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
            return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
        try:
            # game = Game.objects.order_by('-id').first()
            data = json.loads(request.body)
            game_id = data.get('id')
            game = get_object_or_404(Game, id=game_id)
            if not game:
                return JsonResponse({'error': 'No game found to update.'}, status=404)

            #game_id = data.get('gameID')
            #print(game_id)
            #game = get_object_or_404(Game, id=game_id)
            
            game.mode = data.get('mode')
            game.scorep1 = data.get('scorep1')
            game.scorep2 = data.get('scorep2')
            game.state = 'active'
            if (game.scorep1 == 10):
                game.state = 'end'
                game.player1.win += 1
                game.player1.rank += 50 + (game.scorep1 - game.scorep2) * 20
                game.player1.save()
                game.player2.lose += 1
                game.player2.rank += -50 - (game.scorep1 - game.scorep2) * 10
                game.player2.save()
            if (game.scorep2 == 10):
                game.state = 'end'
                game.player2.win += 1
                game.player2.rank += 50 + (game.scorep2 - game.scorep1) * 20
                game.player2.save()
                game.player1.lose += 1
                game.player1.rank += -50 - (game.scorep2 - game.scorep1) * 10
                game.player1.save()

            game.save()
            return JsonResponse({'message': 'Registration successful'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def getIsPlayer(request):
    if request.method == "POST":
        if request.session.get('csrf') != request.COOKIES.get('csrftoken'):
            return JsonResponse({'error': 'Invalid CSRF token'}, status=400)
        try:
            # game = Game.objects.order_by('-id').first()
            data = json.loads(request.body)
            id = data.get('id')
            player = data.get('player')
            game = get_object_or_404(Game, id=id)
            if not game:
                return JsonResponse({'error': 'No game found to update.'}, status=404)

            if game.state == 'active' or game.state == 'waiting':
                if (player == game.player1.username):
                    return JsonResponse({'message': 'isFirstPlayer'}, status=200)
                elif (player == game.player2.username):
                    return JsonResponse({'message': 'isSecondePlayer'}, status=200)
                else:
                    return JsonResponse({'message': 'isSpec'}, status=200)
            return JsonResponse({'message': 'end'}, status=200)
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
