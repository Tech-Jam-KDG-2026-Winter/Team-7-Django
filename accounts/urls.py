# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<str:page_name>/', views.render_page, name='render_page'),
]
