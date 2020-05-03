from django.db import models
from django.utils import timezone


class MouseConfig(models.Model):
    dpi = models.IntegerField(null=True, editable=True)
    edpi = models.IntegerField(null=True, editable=True)
    usb_rate = models.IntegerField(null=True, editable=True)
    win_sens = models.IntegerField(null=True, editable=True)
    game_sens = models.FloatField(null=True, editable=True)
    zoom_sens = models.FloatField(null=True, editable=True)
    raw_input = models.BooleanField(null=True, editable=True)
    mouse_acceleration = models.FloatField(null=True, editable=True)

    def __str__(self):
        return f'Настройки мыши - Игра: {self.playerconfig.game.name}, игрок: {self.playerconfig.player.nickname}'


class VideoConfig(models.Model):
    resolution_width = models.IntegerField(null=True, editable=True)
    resolution_height = models.IntegerField(null=True, editable=True)
    aspect_ration_width = models.IntegerField(null=True, editable=True)
    aspect_ration_height = models.IntegerField(null=True, editable=True)
    frequency = models.IntegerField(null=True, editable=True)
    dimension = models.CharField(max_length=100, null=True, editable=True)

    # def __str__(self):
    #     return f'Видео конфиг - Игра: {self.playerconfig.game.name}, игрок: {self.playerconfig.player.nickname}'


class CrosshairConfig(models.Model):
    crosshair_settings = models.TextField(null=True, editable=True)


class ViewModelConfig(models.Model):
    viewmodel_settings = models.TextField(null=True, editable=True)


class StartUpSettings(models.Model):
    startup_settings = models.TextField(null=True, editable=True)


class PlayerConfig(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    mouse_config = models.OneToOneField(MouseConfig, on_delete=models.CASCADE, null=True, blank=True)
    video_config = models.OneToOneField(VideoConfig, on_delete=models.CASCADE, null=True, blank=True)
    crosshair_config = models.OneToOneField(CrosshairConfig, on_delete=models.CASCADE, null=True, blank=True)
    viewmodel_config = models.OneToOneField(ViewModelConfig, on_delete=models.CASCADE, null=True, blank=True)
    startup_config = models.OneToOneField(StartUpSettings, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('game', 'player',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Конфиг: {self.game.name}, игрок: {self.player.nickname}'

    def __repr__(self):
        return f'<PlayerConfig(Game: {self.game.name}, Player: {self.player.nickname})>'
