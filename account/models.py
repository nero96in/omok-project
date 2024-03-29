from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from omok_main.models import Room

class UserManager(BaseUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(*args, **kwargs)


class User(AbstractUser):
    email = models.EmailField(
        max_length=255,
        # unique=True,
    )

    nickname = models.CharField(
        max_length=30,
        unique=True,
        null=True,
    )

    win = models.IntegerField(
        default=0,
        null=True,
    )

    draw = models.IntegerField(
        default=0,
        null=True,
    )

    lose = models.IntegerField(
        default=0,
        null=True,
    )

    current_room = models.CharField(
        max_length=255,
        default='',
        null=True,
    )

    rank = models.IntegerField(
        default=0,
    )
    
    objects = UserManager()

    def __str__(self):
        return self.username