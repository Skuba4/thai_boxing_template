import uuid
from django.db import models
from django.urls import reverse

from users.models import User


class Room(models.Model):
    uuid_room = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, blank=False)
    boss = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boss_rooms')
    judges = models.ManyToManyField(User, related_name='judges_rooms', through='RoomJudges')

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['boss']),
        ]

    def __str__(self):
        return 'Таблица ROOM'

    def get_absolute_url(self):
        return reverse('referee:detail_room', kwargs={'uuid_room': self.uuid_room})


class RoomJudges(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_judges')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_judges')
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'user'], name='unique_room_user')
        ]

    def __str__(self):
        return 'Промежуточная таблица ROOM-USER'


class Fight(models.Model):
    class Winner(models.TextChoices):
        FIGHTER_1 = 'fighter_1', 'Боец 1'
        FIGHTER_2 = 'fighter_2', 'Боец 2'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='fights')
    number_fight = models.PositiveIntegerField(blank=False)
    fighter_1 = models.CharField(max_length=50, blank=False)
    fighter_2 = models.CharField(max_length=50, blank=False)
    winner = models.CharField(max_length=10, choices=Winner.choices, blank=True, null=True)

    class Meta:
        ordering = ['room', 'number_fight']
        constraints = [
            models.UniqueConstraint(fields=['room', 'number_fight'], name='unique_number_fight_room')
        ]
        indexes = [
            models.Index(fields=['room', 'number_fight']),
            models.Index(fields=['fighter_1']),
            models.Index(fields=['fighter_2']),
        ]

    def __str__(self):
        return 'Таблица FIGHT'


class Notes(models.Model):
    class Winner(models.TextChoices):
        RED = "red", "Красный угол"
        BLUE = "blue", "Синий угол"

    fight = models.ForeignKey(Fight, on_delete=models.CASCADE, related_name='notes')
    data = models.DateField(auto_now_add=True)
    judge = models.CharField(max_length=100)
    round_number = models.IntegerField()
    red_fighter = models.CharField(max_length=100)
    blue_fighter = models.CharField(max_length=100)
    red_remark = models.CharField(max_length=100)
    blue_remark = models.CharField(max_length=100)
    winner = models.CharField(max_length=10, choices=Winner.choices, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fight', 'judge', 'round_number'], name='unique_fight_round')
        ]
        indexes = [
            models.Index(fields=['round_number']),
        ]

    def __str__(self):
        return 'Таблица NOTES'
