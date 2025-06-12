from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    club = models.CharField(max_length=100, null=True, blank=True, verbose_name='Клуб')
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    is_premium = models.BooleanField(default=False, verbose_name="Премиум-доступ")
    premium_until = models.DateField(blank=True, null=True, verbose_name="Подписка до")
