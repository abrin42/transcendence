from django.urls import path, include
from . import views
app_name = "friend"

urlpatterns = [
    path('',  views.index, name='index'),
    path('add/',  views.add, name='add'),
    path('delete/<int:id_friendship>',  views.delete_friend, name='del'),

    path('pending/', views.pending, name='pending'),
    path('accept/<int:id_friendship>', views.accept, name='accept'),
    path('refuse/<int:id_friendship>', views.refuse, name='refuse'),
    path('refused/', views.refused, name='refused'),
    path('list/', views.list, name='list'),
]
