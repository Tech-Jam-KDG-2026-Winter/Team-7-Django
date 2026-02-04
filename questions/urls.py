from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionBatchView.as_view(), name='questions_index'),
    path('<int:pk>/answer/', views.QuestionBatchView.as_view(), name='answer_question'),
]
