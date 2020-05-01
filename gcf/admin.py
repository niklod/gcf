from django.contrib import admin
from gcf.models import User, Player, Game, PlayerConfig, MouseConfig, VideoConfig, CrosshairConfig, StartUpSettings


class PlayerAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class GameAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(User)
admin.site.register(PlayerConfig)
admin.site.register(MouseConfig)
admin.site.register(VideoConfig)
admin.site.register(CrosshairConfig)
admin.site.register(StartUpSettings)
