from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskDashboardView.as_view(), name='index'),
    path('<int:pk>/complete/', views.TaskUpdateView.as_view(), name='complete_task'),
]
