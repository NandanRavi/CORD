from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Room, Topic, Message
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, UserForm
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
            messages.error(request, "Please Check your Username.")

        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            author = str(request.user)
            messages.success(request, f'{author.upper()} We Welcome you on Our App')
            return redirect('home')
        else:
            messages.error(request, 'Password is wrong....')
    
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
                form.add_error('Username', 'Username Already Exist!!!')
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
            messages.error(request, "Don't have an account Register Yourself!!!")

    context = {'form':form}
    return render(request, 'base/login_register.html', context)






def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request,'base/home.html', context)


def profiles(request):
    profiles = User.objects.all()
    context = {'profiles':profiles}
    return render(request, 'base/profiles.html', context)




def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
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


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()

    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context ={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
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
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Chal be Nikal Idhar se')

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not Authorised')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {'obj':message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/update_user.html', context)


def topicsPage(request):
    topics = Topic.objects.filter()
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)