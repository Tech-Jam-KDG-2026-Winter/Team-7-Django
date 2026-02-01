#########リダイアレクト先の設定##########


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')

        if User.objects.filter(name=name).exists():
            return render(request, 'accounts/signup.html', {'error': 'この名前は既に使用されています。'})

        User.objects.create(
            username=name,
            name=name,
            password=make_password(password),
            height=height,
            weight=weight,
            gender=gender,
            birth_date=birth_date
        )
        return redirect('login')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(name=name)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('index') ################# リダイアレクト先（仮） ##################

            else:
                error = "パスワードが一致しません。"
        except User.DoesNotExist:
            error = "ユーザーが存在しません。"
            
        return render(request, 'accounts/login.html', {'error': error})

    return render(request, 'accounts/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')
