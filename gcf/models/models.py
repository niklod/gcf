from django.db import models
from django.utils import timezone
from ..utils.slug_generator import generate_slug


class User(models.Model):
    username = models.CharField(max_length=80, null=False, unique=True)
    email = models.EmailField(max_length=125, null=False)
    first_name = models.CharField(max_length=80, null=True)
    last_name = models.CharField(max_length=80, null=True)
    created_at = models.DateTimeField(editable=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'<User(username: {self.username}, id: {self.id})>'


class Game(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    slug = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(editable=False, null=False, default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<(Game: {self.name}, id: {self.id})>'


class Player(models.Model):
    name = models.CharField(max_length=100, null=False)
    nickname = models.CharField(max_length=100, null=False, unique=True)
    age = models.IntegerField(null=True)
    description = models.CharField(max_length=300, null=True)
    slug = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(editable=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    games = models.ManyToManyField(Game)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()

            temp_slug = generate_slug(self.nickname)
            player = Player.objects.filter(slug=temp_slug).all()

            # If we find player with same nickname, generate slug as name + nickname
            if player:
                self.slug = generate_slug(f'{self.name} {self.nickname}')
            else:
                self.slug = temp_slug

        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Player(Name: {self.name}, id: {self.id})>'
