from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.game, name="game"),
    path('insertplayer/', views.insertPlayer, name="insertPlayer"),
    path('update_game/', views.update_game, name='update_game'),
    path('creat_game_local/', views.creat_game_local, name='creat_game_local'),
    
    # path('getgameid/', views.getgameid, name="getgameid"),
]