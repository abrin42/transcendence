from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.game, name="game"),
    path('insertplayer/', views.insertPlayer, name="insertPlayer"),
    path('update_game/', views.update_game, name='update_game'),
    
    # path('getgameid/', views.getgameid, name="getgameid"),
]