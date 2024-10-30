from django.urls import path
from . import views
from . import jwt
from . import utils
from . import update

app_name = "player"

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('tfa/', views.tfa_view, name='tfa'),
    path('otp/', views.otp_view, name="otp"),
    path('login42/', views.login42_view, name="login42"),
    path('auth/42/callback/', views.auth_42_callback, name='auth_42_callback'),
    path('logout/', views.logout_view, name='logout'),
    
    path('get_csrf_token/', utils.get_csrf_token, name='get_csrf_token'),
    path('verify_user/', utils.verify_user, name='verify_user'),
    path('verify-jwt/', jwt.verify_jwt, name='verify_jwt'),
    path('connected_user/', utils.connected_user, name='connected_user'),
    path('get_all_user/', utils.get_all_user, name='get_all_user'),

    path('update_language/', update.update_language, name='update_language'),
    path('update_user/', update.update_user, name='update_user'),
    path('update_keys/', update.update_keys, name='update_keys'),
    path('delete_account/', views.delete_account, name='delete_account'),    
    
    path('enter_matchmaking/', views.enter_matchmaking, name='enter_matchmaking'),
    path('quit_matchmaking/', views.quit_matchmaking, name='quit_matchmaking'),
    path('get_match/', views.get_match, name='get_match'),
    
]