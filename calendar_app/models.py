from django.db import models
from django.conf import settings


class Record(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='records'
    )
    plus_calorie = models.FloatField(default=0.0, help_text='Calories gained')
    minus_calorie = models.FloatField(default=0.0, help_text='Calories burned')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'records'
        verbose_name = 'Record'
        verbose_name_plural = 'Records'
        ordering = ['-created_at']
        
        unique_together = [['user', 'created_at']]

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    @property
    def net_calorie(self):
        return self.plus_calorie - self.minus_calorie