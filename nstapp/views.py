from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# '/' 홈에서 사용자가 있다면 메인페이지로,
# 없다면 로그인 페이지로 연결한다.
def home(request):
    user = request.user.is_authenticated

    if user:
        return redirect('/upload')
    else:
        return redirect('/sign-in')


# 메인페이지 함수
@login_required
def upload(request):
    return render(request, 'index.html')


@login_required
def camera(request):
    return render(request, 'camera.html')
