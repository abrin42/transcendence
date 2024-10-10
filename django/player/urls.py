from django.urls import path
from . import views
from . import jwt

app_name = "player"

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('tfa/', views.tfa_view, name='tfa'),
    path('otp/', views.otp_view, name="otp"),
    path('account/', views.account_view, name="account"),
    path('login42/', views.login42_view, name="login42"),
    path('auth/42/callback/', views.auth_42_callback, name='auth_42_callback'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-jwt/', jwt.verify_jwt, name='verify_jwt'),
    path('update/', views.update_view, name='update'),
    path('update_password/', views.update_password_view, name='update_password'),
    path('delete_account/', views.delete_account_view, name='delete_account'),
    path('connected_user/', views.connected_user, name='connected_user'),
    path('update_language/', views.update_language, name='update_language'),
    path('get_all_user/', views.get_all_user, name='get_all_user'),
    path('enter_matchmaking/', views.enter_matchmaking, name='enter_matchmaking'),
    path('quit_matchmaking/', views.quit_matchmaking, name='quit_matchmaking'),
    path('get_match/', views.get_match, name='get_match'),
    
]