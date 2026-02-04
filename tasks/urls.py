from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskDashboardView.as_view(), name='task_list'),
    path('<int:pk>/complete/', views.TaskUpdateView.as_view(), name='update_task'),
]
