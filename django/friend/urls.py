from django.urls import path, include
from . import views
app_name = "friend"

urlpatterns = [
    path('',  views.index, name='index'),
    path('add/',  views.add, name='add'),
    path('delete/',  views.delete, name='delete'),
    path('pending/', views.pending, name='pending'),
    #path('accept', views.accept, name='accept'),
    path('refuse', views.refuse, name='refuse'),
    path('refused/', views.refused, name='refused'),
    path('list/', views.list, name='list'),
    path('help/', views.help, name='help'),
]