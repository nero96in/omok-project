from django.shortcuts import render
from django.utils.safestring import mark_safe
from omok_main.models import Room
import json

# Create your views here.
def home(request):
    return render(request, 'omok_main/home.html')

def index(request):
    return render(request, 'omok_main/index.html', {})

def room(request, room_name):
    username = None
    room = Room.objects.get(room_name=room_name)
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'omok_main/demoPlay.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user_name_json': mark_safe(json.dumps(username)),
        'room': room
    })