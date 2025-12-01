from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Ingredient
from .forms import RoomForm

# Create your views here.

# rooms =[
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me!'},
#     {'id':3, 'name':'Yippe room!'},
# ]

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Username OR Password does not exist')

    context = {'page': page}

    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # we want to be able to access the user right away
            #we want to clean up the data
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
            # to add more different type of errors in registration

    return render(request, 'base/login_register.html', {'form': form})

def home(request): #request is http object, what ckind of tada request is sending
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(host__username__icontains=q) |
                                Q(description__icontains=q)) # kakvo containva v searcha
    
    ingredients_filter = request.GET.getlist('ingredients')
    ingredients = Ingredient.objects.all()

    if ingredients_filter:
        recipes = Room.objects.all()
        for ing in ingredients_filter:
            ingredient_obj = Ingredient.objects.get(id=ing)
            recipes = recipes.filter(ingredients__icontains=ingredient_obj.name)
    else:
        recipes = Room.objects.all()

    topics = Topic.objects.all() #taka dostypvame db-to s queryta
    room_count = rooms.count() #gets the lenght of a query

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'ingredients': ingredients, 'selected_ingredients': [int(i) for i in ingredients_filter] }
    return render(request, 'base/home.html', context)


def room(request, pk): #pk = primary key

    room = Room.objects.get(id=pk)     
    ingredients = Ingredient.objects.all()   
    context = {'room': room, 'ingredients': ingredients}
    

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        print("POST RECEIVED")  # DEBUG LINE
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        else:
            print("FORM ERRORS:", form.errors)

    return render(request, 'base/room_form.html', {'form': form})


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form =  RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room) #this is replacing a room, not creating a nrew one
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})