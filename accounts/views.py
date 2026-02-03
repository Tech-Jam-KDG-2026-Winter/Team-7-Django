# accounts/views.py
from django.shortcuts import render
from django.http import Http404

def render_page(request, page_name):
    # 許可するテンプレートをリストで管理
    allowed_pages = ['first', 'check', 'signin', 'signup', 'complete']
    if page_name in allowed_pages:
        return render(request, f'accounts/{page_name}.html')
    else:
        raise Http404("ページが存在しません")
