from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player

@admin.register(Player)
class Player_admin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'nickname', 'rank', 'phone_number', 'win', 'lose', 'email_2fa_active', 'sms_2fa_active')}),
    )