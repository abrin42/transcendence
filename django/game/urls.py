from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.game, name="game"),
    path('insertplayer/', views.insertPlayer, name="insertPlayer"),
    # path('getgameid/', views.getgameid, name="getgameid"),
]