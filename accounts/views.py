#########リダイアレクト先の設定##########


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models import User

# Create your views here.
class SignupView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        # name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # height = request.POST.get('height')
        # weight = request.POST.get('weight')
        # gender = request.POST.get('gender')
        # birth_date = request.POST.get('birth_date')

        # if User.objects.filter(name=name).exists():
        #     return render(request, 'accounts/signup.html', {'error': 'この名前は既に使用されています。'})

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/signup.html', {'error': 'このメールアドレスは既に使用されています。'})

        user = User.objects.create(
            password=make_password(password),
            email=email,
        )
        request.session['user_id'] = user.id
        return redirect('index')################# リダイアレクト先（仮） ##################

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('index') ################# リダイアレクト先（仮） ##################

            else:
                error = "パスワードが一致しません。"
        except User.DoesNotExist:
            error = "ユーザーが存在しません。"
            
        return render(request, 'accounts/login.html', {'error': error})

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login')
