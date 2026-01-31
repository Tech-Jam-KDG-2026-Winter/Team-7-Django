from django.db import models

# Create your models here.
class User(models.Model):
    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
        ('other', '未回答'),
    ]

    name = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
