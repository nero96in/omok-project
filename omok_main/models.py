from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)
    player1 = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name='player1_test',
        null=True
        )
    player2 = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name='player2_test',
        null=True
        )
    winner = models.CharField(max_length=255, null=True)
    is_playing = models.BooleanField(default=False)
    is_waiting = models.BooleanField(default=False)
    omok_board = models.TextField(null=True, default='')
            