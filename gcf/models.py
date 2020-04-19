from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=80, null=False)
    email = models.EmailField(max_length=125, null=False)
    first_name = models.CharField(max_length=80, null=True)
    last_name = models.CharField(max_length=80, null=True)
    created_at = models.DateTimeField(editable=False, null=False)
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


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=True)
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Player(Name: {self.name}, id: {self.id})>'
