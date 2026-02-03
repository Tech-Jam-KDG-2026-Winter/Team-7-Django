from django.shortcuts import render, redirect
from django.views import View
from .models import Question, UserAnswer
from tasks.models import Category, Task
from accounts.models import User

# Create your views here.
class QuestionBatchView(View):
    def get(self, request): # 質問一覧表示
        user_id = request.session.get('user_id')
        if not user_id:
          return redirect('login')

        questions = Question.objects.all()
        return render(request, 'questions.html', {'questions': questions})

    def post(self, request, pk): # 質問回答・保存
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
            
        user = User.objects.get(id=user_id)
        question = Question.objects.get(id=pk)
        
        answer_str = request.POST.get('answer')
        is_yes = (answer_str == 'yes')

        UserAnswer.objects.update_or_create(
            user=user,
            question=question,
            defaults={'answer': is_yes}
        )

        total_questions = Question.objects.count()
        answered_count = UserAnswer.objects.filter(user=user).count()

        if total_questions == answered_count:
            self.create_recommended_task(user)
            return redirect('index') # タスク一覧へ移動

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
            task, created = Task.objects.get_or_create(
                user=user,
                category=best_category,
                phase='Medium',
                content=f'{best_category.title} に基づくおすすめタスク',
                defaults={'calorie': 0.0}
            )
            return task
        return None
