from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.PlayerList.as_view()),
    path('<int:pk>', views.PlayerDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
