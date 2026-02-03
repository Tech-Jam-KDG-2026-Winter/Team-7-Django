from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from django.utils import timezone
from .models import Task, TaskDailyAchieved
from accounts.models import User
from questions.views import QuestionBatchView

# Create your views here.
class TaskDashboardView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login')

        # おすすめタスクを取得し、それに基づいてフィルタリング
        recommended_task = QuestionBatchView.create_recommended_task(user)
        if recommended_task:
            tasks = Task.objects.filter(user=user, category=recommended_task.category)
        else:
            tasks = Task.objects.filter(user=user)
        
        return render(request, 'index.html', {'tasks': tasks, 'user': user})

class TaskUpdateView(View):
    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        try:
            user = User.objects.get(id=user_id)
            task = Task.objects.get(id=pk, user=user)
        except (User.DoesNotExist, Task.DoesNotExist):
            return redirect('index')

        task.is_achieved = True
        task.save()

        today = timezone.now().date()
        if not TaskDailyAchieved.objects.filter(user=user, task=task, created_at=today).exists():
            TaskDailyAchieved.objects.create(user=user, task=task)
            
        return redirect('index')
