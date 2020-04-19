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
