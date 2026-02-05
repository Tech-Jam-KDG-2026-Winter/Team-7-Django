from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, TaskDailyAchieved
from accounts.models import User
from questions.views import QuestionBatchView

# Create your views here.
class TaskDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        recommended_task = QuestionBatchView.create_recommended_task(user)
        if recommended_task:
            tasks = Task.objects.filter(user=user, category=recommended_task.category)
        else:
            tasks = Task.objects.filter(user=user)
        
        return render(request, 'task_list.html', {'tasks': tasks, 'user': user})

class TaskUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        
        try:
            task = Task.objects.get(id=pk, user=user)
        except Task.DoesNotExist:
            return redirect('task_list')
        
        task.is_achieved = not task.is_achieved
        task.save()

        today = timezone.now().date()
        
        if task.is_achieved:
            TaskDailyAchieved.objects.get_or_create(user=user, task=task, created_at=today)
        else:
            TaskDailyAchieved.objects.filter(user=user, task=task, created_at=today).delete()
            
        return redirect('task_list')
