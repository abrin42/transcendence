from django.contrib import admin
from .models import Friendship
# Register your models here.

@admin.register(Friendship)
class Friendship_admin(admin.ModelAdmin):
    list_display = ["user", "friend", "status","id"]
    pass
