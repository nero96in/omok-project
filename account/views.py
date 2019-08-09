from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .form import LoginForm, SignupForm
from .models import User
from django.db import connection

# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
        if signup_form.is_valid():
            # 유저를 생성 후 해당 User를 로그인 시킨다
            user = signup_form.save()
            django_login(request, user)
            return redirect('/')
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        # 로그인 성공 후 이동할 URL. 주어지지 않으면 None
        next = request.GET.get('next')

        # Data bounded form인스턴스 생성
        # AuthenticationForm의 첫 번째 인수는 해당 request가 되어야 한다
        login_form = LoginForm(request=request, data=request.POST)

        # 유효성 검증에 성공할 경우
        # AuthenticationForm을 사용하면 authenticate과정까지 완료되어야 유효성 검증을 통과한다
        if login_form.is_valid():
            # AuthenticatonForm에서 인증(authenticate)에 성공한 유저를 가져오려면 이 메서드를 사용한다
            user = login_form.get_user()
            # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
            django_login(request, user)
            # next가 존재하면 해당 위치로, 없으면 Post목록 화면으로 이동
            return redirect(next if next else '/')
        # 인증에 실패하면 login_form에 non_field_error를 추가한다
        login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'login.html', context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    return render(request, 'signup.html')

def ranking(request):
    all_user = User.objects.all()
    sorted_all_users_queries = User.objects.all().order_by('-win')
    page = request.GET.get('page', 1)
    paginator = Paginator(sorted_all_users_queries, 20)
    rankings = range(1, len(sorted_all_users_queries)+1)

    try:
        sorted_users = paginator.page(page)
    except PageNotAnInteger:
        sorted_users = paginator.page(1)
    except EmptyPage:
        sorted_users = paginator.page(paginator.num_pages)
    
    # paginator=Paginator(sorted_all_users_queries,7)
    # page=request.GET.get('page')
    # posts=paginator.get_page(page)
    
    if request.method == "GET":   
        return render(request, "ranking.html",{

                'sorted_users':sorted_users,
                })
    elif request.method == "POST":
        query = request.POST['query']
        if query:
            search_nick = all_user.filter(nickname=query)
        return render(request, "ranking.html",{
                'all_user':all_user, 
                'search_nick' : search_nick, 
                'sort' : sorted_all_users_queries,
                })
        


# def search(request):
#     user = User.objects.all()
#     saved_nick=User.objects.all()
#     search_nick=request.GET.get('bar','')

#     if search_nick:
#         search_nick=user.filter(saved_nick=search_nick)

#     return render(request, "ranking.html",{
#             'user' : user, 
#             'saved_nick' : saved_nick,
#             'search_nick' : search_nick, 
#         })




