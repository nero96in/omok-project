from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model

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
    objects = UserManager()

    def __str__(self):
        return self.username