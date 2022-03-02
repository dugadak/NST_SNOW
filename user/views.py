from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import re


# 회원가입('sign-up/') 함수
def sign_up_view(request):
    # 로그인 상태인 유저가 있다면 '/' 로 이동하고, 없다면 회원가입 페이지를 띄워준다.
    if request.method == 'GET':
        user = request.user.is_authenticated

        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')

    # html 에서 회원가입 정보 가져오기
    elif request.method == 'POST':
        # Abstrctuser 상속 시 인증과 관련된 username 테이블로 userid 를 받는다.
        email = request.POST.get('username', '')
        nickname = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_check = request.POST.get('password_check', '')

        # 예외처리 : 공란 일때 회원가입 방지
        if email == '' or nickname == '' or password == '':
            return render(request, 'user/signup.html', {'error': '필수항목을 입력해주세요.'})

        else:
            # 예외처리 : 패스워드 불일치
            if password != password_check:
                return render(request,'user/signup.html', {'error': '패스워드가 일치하지 않습니다.'})

            # 예외처리 : 이미 존재하는 아이디 확인
            exist_userid = get_user_model().objects.filter(username=email)

            if exist_userid:
                return render(request, 'user/signup.html', {'error': '이미 존재하는 이메일입니다.'})

            # 예외처리 : 이미 존재하는 이메일 확인
            exist_useremail = get_user_model().objects.filter(email=nickname)

            if exist_useremail:
                return render(request, 'user/signup.html', {'error': '이미 존재하는 닉네임입니다.'})

            # 예외처리 : 이메일 형식 확인('@', '.' 이 있는지 확인)
            email_form = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            check_email = email_form.match(email)
            print(check_email)

            if check_email is None:
                return render(request, 'user/signup.html', {'error': '이메일 형식이 아닙니다.'})

            # 예외사항에 해당하지 않는다면 usermodel에 유저를 생성한다.
            else:
                UserModel.objects.create_user(username=email, password=password, email=nickname)
                return redirect('/sign-in')

            # + 사항 : 회원가입 실패 시 입력값 유지


# 로그인 함수
def sign_in_view(request):
    if request.method == 'POST':
        email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 사용자 불러오기
        # me = get_user_model().objects.filter(user_id=userid, password=password)
        me = auth.authenticate(request, username=email, password=password)
        print(email)
        print(password)
        print(me)
        # 사용자가 있다면, 세션에 인증된 사용자 ID 저장
        # 사용자가 없다면 error 메세지 보여줌
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': '이메일과 패스워드가 일치하는 사용자가 없습니다. 다시 입력해주세요.'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

        # + 사항 : abstractuser 상속받고 user_id 라는 필드를 생성하여도 인증에 관련된 부분을
        # 따로 지정해주지 않으면 로그인 시 auth.login 을 사용할 수 없음
        # 해결방법 : userid -> username(인증가능) 테이블로 저장
        # 다른 해결방법이 있을까?


# 로그아웃 함수
@login_required
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('/')




