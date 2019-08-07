from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .form import LoginForm, SignupForm

# Create your views here.

def home(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
        if signup_form.is_valid():
            # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
            signup_form.signup()
            return redirect('/')
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'signup.html', context)

# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
#             auth.login(request, user)
#             return redirect('/')

#         if request.POST['password1'] != request.POST['password2']:
#             return render(request, 'signup.html', {'error':'패스워드가 다르다'})

#     return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 가져온 username과 password에 해당하는 User가 있는지 판단한다
            # 존재할경우 user변수에는 User인스턴스가 할당되며,
            # 존재하지 않으면 None이 할당된다
            user = authenticate(
                username=username,
                password=password
            )
            # 인증에 성공했을 경우
            if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)
                # Post목록 화면으로 이동
                return redirect('/')
            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'login.html', context)

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'login.html', {'error': 'username or password is incorrect.'})
#     else:
#         return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    return render(request, 'signup.html')