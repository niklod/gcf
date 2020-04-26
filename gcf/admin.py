from django.contrib import admin
from gcf.models import User, Player, Game


class PlayerAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class GameAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(User)
