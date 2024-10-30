from django.urls import path
from . import views


app_name = "game"

urlpatterns = [
    path('', views.game, name="game"),
    path('insertplayer/', views.insertPlayer, name="insertPlayer"),
    path('update_game/', views.update_game, name='update_game'),
    path('create_game_local/', views.create_game_local, name='create_game_local'),
    path('getGameInfo/', views.getGameInfo, name='getGameInfo'),
    path('getIsPlayer/', views.getIsPlayer, name='getIsPlayer'),
    path('get_all_games/', views.get_all_games, name="get_all_games"),
    path('createFalsePlayer/', views.createFalsePlayer, name='createFalsePlayer'),
    path('createOneFalsePlayer/', views.createOneFalsePlayer, name='createOneFalsePlayer'),
    path('setGameRank/', views.setGameRank, name='setGameRank'),


    # path('getgameid/', views.getgameid, name="getgameid"),
]