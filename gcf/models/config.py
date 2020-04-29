from django.db import models
from django.utils import timezone


class MouseConfig(models.Model):
    dpi = models.IntegerField(null=True, editable=True)


class PlayerConfig(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    mouse_config = models.OneToOneField(MouseConfig, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('game', 'player',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Игра: {self.game.name}, игрок: {self.player.nickname}'

    def __repr__(self):
        return f'<PlayerConfig(Game: {self.game.name}, Player: {self.player.nickname})>'
