from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.
def home(request):
    return render(request, 'omok_main/home.html')

def index(request):
    return render(request, 'omok_main/index.html', {})

def room(request, room_name):
    return render(request, 'omok_main/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })