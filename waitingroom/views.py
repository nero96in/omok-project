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
    if request.method == "GET":
        search_room = Room.objects.all()
        search_word = request.GET.get('search_word','')
        if search_word:
            search_room = all_room.filter(room_name=search_word)
        
        
        return render(request, 'waitingroom.html', {
            'all_room': all_room,
            'search_word' : search_word,
            'search_room':search_room,
            'error':" Not Found !",
            
            })
            
    elif request.method == "POST":
        check_room = Room.objects.all()
        query = request.POST['check_room']
        check_room = all_room.filter(room_name=query)
        username = None
        if check_room:
            # check_room = request.POST['check_room']
            # check_room = int(check_room)
            return render(request, 'waitingroom.html',{
                'check_room' : check_room , #이미 있는방
                'error_post' : " 이(가) 이미 존재합니다",
                'all_room': all_room,
            })
        else:
            print(query)
            # query = int(query)
            new_room = Room(room_name=query)
            new_room.save()
            return render(request, 'waitingroom.html',{
                'query' : query ,#방 생성
                'error_post' : "이(가) 생성되었습니다.",
                'all_room': all_room,
            })
        
        


def enter_room(request, room_name):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'omok_main/demoPlay.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'user_name_json': mark_safe(json.dumps(username)),
        })

    




