from django.shortcuts import render
from .models import Room

# Create your views here.

# rooms =[
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me!'},
#     {'id':3, 'name':'Yippe room!'},
# ]


def home(request): #request is http object, what ckind of tada request is sending
    rooms = Room.objects.all() #taka dostypvame db-to s queryta
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk): #pk = primary key

    room = Room.objects.get(id=pk)        
    context = {'room': room}
    return render(request, 'base/room.html', context)
