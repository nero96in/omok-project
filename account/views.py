from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from .form import LoginForm, SignupForm
from .models import User
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
    # dddddddddddddddd
    
    # win_query = User.objects.all().values_list('win', flat=True) 
    win_query = User.objects.values_list('win', flat=True).order_by('-win')
    nickname_query = User.objects.order_by('-win').values_list('nickname',flat=True)
    win=[]
    nickname=[]
    for i in range(0,len(win_query)):
        win.append(win_query[i])
        nickname.append(nickname_query[i])
    print(nickname)
    print(win)
    count = 0 
    rank = []
    for i in range(0,len(win)):
        if i > 0:
            if win[i] == win[i-1]:
                rank.append(rank[count])
                continue
        rank.append(i+1)
        count = i
    print(rank)
    # win=User.objects.all().order_by('-win')
    for i in range(0, len(win)):
        some_user = User.objects.get(nickname=nickname[i])
        some_user.rank = rank[i]
        some_user.save()
    length = len(win)
    
        
    
    # ddddddddddddddddddd


    sort=User.objects.all().order_by('rank')
    paginator = Paginator(sort, 1000)
    page = request.POST.get('page','1')
    try:
        sort = paginator.page(page)
    except PageNotAnInteger:
        sort = paginator.page(1)
    except EmptyPage:
        sort = paginator.page(paginator.num_pages)

    
    
    if request.method == "GET":   
        return render(request, "ranking.html",{
                'all_user':all_user, 
                'sort':sort,
                'length':length,
                })
    elif request.method == "POST":
        query = request.POST['query']
        if query:
            search_nick = all_user.filter(nickname=query)
        return render(request, "ranking.html",{
                'all_user':all_user, 
                'search_nick' : search_nick, 
                'sort':sort,
                })
        



def search(request):
    user = User.objects.all()   
    saved_nick=User.objects.all()
    search_nick=request.GET.get('bar','')

    if search_nick:
        search_nick=user.filter(saved_nick=search_nick)

    return render(request, "ranking.html",{
            'user':user, 
            'saved_nick':saved_nick,
            'search_nick' : search_nick, })


# def post_list(request):
#     post_list = User.objects.all().order_by('-created_date')
#     paginator = Paginator(post_list, 10)
#     page = request.POST.get('page','1')
#     try:
#         post_list = paginator.page(page)
#     except PageNotAnInteger:
#         post_list = paginator.page(1)
#     except EmptyPage:
#         post_list = paginator.page(paginator.num_pages)

#     context = {'post_list':post_list}
#     return render(request, 'ranking.html', context)

def rank_list_ajax(request): #Ajax 로 호출하는 함수
    sort=User.objects.all().order_by('rank')
    paginator = Paginator(sort, 3)
    page = request.POST.get('page','1')
    nickname = User.objects.all()

    try:
        sort = paginator.page(page)
    except PageNotAnInteger:
        sort = paginator.page(1)
    except EmptyPage:
        sort = paginator.page(paginator.num_pages)

    context = {'sort':sort,
                'nickname':nickname
            }
    return render(request, 'rank_list_ajax.html', context) #Ajax 로 호출하는 템플릿은 _ajax로 표시.




