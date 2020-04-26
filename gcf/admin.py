from django.contrib import admin
from gcf.models import User, Player


class PlayerAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Player,PlayerAdmin)
admin.site.register(User)
