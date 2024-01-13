from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Room, Topic, Message
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST['Username'].lower()
        password = request.POST['Password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Tu kon hai be")

        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            messages.success(request, 'Swagat hai Bidu Tera')
            return redirect('home')
        else:
            messages.error(request, 'Password Galat nhi Daalne ka')
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST['Username'].lower()
            if User.objects.filter(username=username).exists():
                form.add_error('Username', 'Naam Chori mat kar Panga ho jaayega')
            else:
                user = form.save(commit=False)
                user.username = username
                user.save()
                login(request, user)
                return redirect('home')
            # user = form.save(commit=False)
            # user.username = user.username.lower()
            # user.save()
            # login(request, user)
            # return redirect('home')
        else:
            messages.error(request, 'Zaldi hai kahi jaane ka hai Nahi toh Aaram se register kar')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)






def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request,'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    particpants = room.participants.all()


    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'particpants':particpants}
    return render(request,'base/room.html', context)


@login_required(login_url='login')
def create_Room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_Room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Chal be Nikal Idhar se')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_Room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Chal be Nikal Idhar se')

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_Message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Chal be Nikal Idhar se')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {'obj':message}
    return render(request, 'base/delete.html', context)