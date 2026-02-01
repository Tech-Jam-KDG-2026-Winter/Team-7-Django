from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
        ('other', '未回答'),
    ]

    name = models.CharField(max_length=100, unique=True)
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    birth_date = models.DateField()

    def __str__(self):
        return self.name
