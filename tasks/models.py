from django.db import models
from django.conf import settings


class Category(models.Model):
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Task(models.Model):
    
    PHASE_CHOICES = [
        ('Large', 'Large'),
        ('Medium', 'Medium'),
        ('Small', 'Small'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    phase = models.CharField(max_length=10, choices=PHASE_CHOICES)
    content = models.TextField()
    calorie = models.FloatField(default=0.0)
    is_achieved = models.BooleanField(default=False)

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"


class TaskDailyAchieved(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_achievements'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='daily_achievements'
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'task_daily_achieved'
        verbose_name = 'Task Daily Achievement'
        verbose_name_plural = 'Task Daily Achievements'
        ordering = ['-created_at']
        
        unique_together = [['user', 'task', 'created_at']]

    def __str__(self):
        return f"{self.user.username} - {self.task.content[:30]} - {self.created_at}"