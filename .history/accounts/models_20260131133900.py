from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=20)
    birth_date = models.DateField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
