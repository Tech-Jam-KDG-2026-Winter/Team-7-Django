from django.db import models
from django.conf import settings
from tasks.models import Category

class Question(models.Model):
    
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('LOW', 'Low'),
    ]

    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    content = models.TextField()
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES)
    is_yes = models.BooleanField(default=False)

    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-priority', 'id']

    def __str__(self):
        return f"{self.category.title} - {self.content[:50]}"

class UserAnswer(models.Model): # ユーザーの質問回答を保存（＊要確認）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_answers'
        unique_together = ('user', 'question')