from django.contrib import admin
from core.models import Team, Game, CustomUser, Pick

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Pick)
class PickAdmin(admin.ModelAdmin):
    pass



