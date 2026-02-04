from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .models import User

# Create your views here.
class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        username = email

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'このメールアドレスは既に使用されています。'})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('questions_index')################# リダイアレクト先（仮） ##################

class LoginView(View):
    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            target_user = User.objects.get(email=email)
            username = target_user.username
        except User.DoesNotExist:
            return render(request, 'signin.html', {'error': 'ユーザーが存在しません'})

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list') ################# リダイアレクト先（仮） ##################
        else:
                error = "パスワードが一致しません。"
                    
        return render(request, 'signin.html', {'error': error})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
