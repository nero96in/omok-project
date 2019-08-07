from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)
    player1 = models.CharField(max_length=255, null=True)
    player2 = models.CharField(max_length=255, null=True)
    winner = models.CharField(max_length=255, null=True)