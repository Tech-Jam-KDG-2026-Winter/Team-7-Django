from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, UserAnswer
from tasks.models import Category, Task
from accounts.models import User

# Create your views here.
class QuestionBatchView(LoginRequiredMixin,View):
    def get(self, request): # 質問一覧表示

        questions = Question.objects.all()
        return render(request, 'questions.html', {'questions': questions})

    def post(self, request):
        
        user = request.user

        questions = Question.objects.all()
        
        for question in questions:
            answer_val = request.POST.get(f'answer_{question.id}')
            
            if answer_val is not None:
                is_yes = (answer_val == 'yes')
                UserAnswer.objects.update_or_create(
                    user=user,
                    question=question,
                    defaults={'answer': is_yes}
                )
    
        total_questions = questions.count()
        answered_count = UserAnswer.objects.filter(user=user).count()

        if total_questions == answered_count:
            self.create_recommended_task(user)
            return redirect('task_list')
    
        return redirect('questions_index')

    @staticmethod
    def create_recommended_task(user):# カテゴリごとに集計→リコメンド
        categories = Category.objects.all()
        best_category = None
        max_yes_count = -1

        for category in categories:
            yes_count = UserAnswer.objects.filter(
                user=user,
                question__category=category,
                answer=True
            ).count()
            
            if yes_count > max_yes_count:
                max_yes_count = yes_count
                best_category = category
        
        if best_category:
            master_tasks = Task.objects.filter(category=best_category)
            
            for master in master_tasks:
                task, created = Task.objects.get_or_create(
                    user=user,
                    category=best_category,
                    phase=master.phase,
                    content=master.content,
                    calorie=master.calorie
                )
            return task
        return None
