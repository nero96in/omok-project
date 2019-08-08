from django.shortcuts import render ,redirect 
from django.utils.safestring import mark_safe
import json
from omok_main.models import Room
from django import forms
# from .form import Addroom
from django.db.models import Q  

# Create your views here.   

def waitingroom(request):
    all_room = Room.objects.all()
    search_room = Room.objects.all()
    search_word = request.GET.get('search_word','')
    if search_word:
        search_room = all_room.filter(room_name=search_word)
    return render(request, 'waitingroom.html', {
        'all_room': all_room,
        'search_word' : search_word,
        'search_room':search_room,
        'error':" Not Found !"
        
        })


# def signup(request):
#     if request.method == 'POST':
#         signup_form = SignupForm(request.POST)
#         # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
#         if signup_form.is_valid():
#             # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
#             signup_form.signup()
#             return redirect('/')
#     else:
#         signup_form = SignupForm()

#     context = {
#         'signup_form': signup_form,
#     }
#     return render(request, 'signup.html', context)




def addroom(request, room_name):
    # room_name = Addroom.room_name()
    # if Room.objects.filter(room_name=room_name).exists():
    #     raise forms.ValidationError('아이디가 이미 사용중입니다')

    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'omok_main/demoPlay.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user_name_json': mark_safe(json.dumps(username))
    })




