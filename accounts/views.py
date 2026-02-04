#########リダイアレクト先の設定##########


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
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

        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email,
        )
        request.session['user_id'] = user.id
        return redirect('questions_index')################# リダイアレクト先（仮） ##################

class LoginView(View):
    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('questions_index') ################# リダイアレクト先（仮） ##################

            else:
                error = "パスワードが一致しません。"
        except User.DoesNotExist:
            error = "ユーザーが存在しません。"
            
        return render(request, 'login.html', {'error': error})

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login')
