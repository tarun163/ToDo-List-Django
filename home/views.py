from django.shortcuts import render, redirect
from home.models import Task,User
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.


def home(request):
    context = {'success': False}
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        customer = request.user.username
        user = User.objects.filter(username = customer).first()
        print(user.username)
        if request.method == "POST":
            title = request.POST['title']
            desc = request.POST['desc']
            ins = Task(user = user, taskname=title, taskdesc=desc)
            ins.save()
            context = {
                'success': True,
                'message': "your tast has been added",
                'class': "alert-success"
            }
            return render(request, 'index.html', context)
    else:
        context = {
            'success': True,
            'message': "login first",
            'class': "alert-danger"
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html', context)


def tasks(request):
    context = {'success': False}
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        customer = request.user.username
        user = User.objects.filter(username = customer).first()
        print(user.username)
        task = Task.objects.filter(user = user)
        for item in task:
            print(item.taskname)
            
        context = {'tasks': task}
        return render(request, 'tasks.html', context)
    
    else:
        context = {
            'success': True,
            'message': "login first",
            'class': "alert-danger"
        }
        return render(request, 'tasks.html', context)



def delete(request, id):
    alltasks = Task.objects.all()
    print(id)
    Task.objects.get(pk=id).delete()
    task = Task.objects.all()
    context = {
            'success': True,
            'message': "task deleted successfully",
            'class': "alert-success",
            'tasks':task
        }
    return render(request, 'tasks.html', context)


def update(request, id):
    obj = Task.objects.get(pk=id)
    myobj = {
        "title": obj.taskname,
        "desc": obj.taskdesc,
        "id": obj.id
    }
    return render(request, 'update.html', context=myobj)


def edit(request, id):
    if request.user.is_authenticated:
        customer = request.user.username
        user = User.objects.filter(username = customer).first()
        print(user.username)
        
        obj = Task(pk=id)
        obj.title = request.GET['title']
        obj.desc = request.GET['desc']
        import datetime
        update_at = datetime.datetime.now()
        obj.time = update_at
        inses = Task.objects.filter(pk=id).update(taskname=obj.title, taskdesc=obj.desc)
        task = Task.objects.all()
        context = {
            'success': True,
            'message': "task updated successfully",
            'class': "alert-success",
            'tasks':task
        }
        return render(request, 'tasks.html', context)
    return redirect('home')    

def search(request):
    if request.method == 'GET':
        search = request.GET['q']
        alltasks = Task.objects.all().filter(taskname=search)
        print(alltasks)
        context = {'tasks': alltasks}
        return render(request, 'tasks.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        context = {'form': form}
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            return render(request, 'login.html', context)

    else:
        form = AuthenticationForm()
        print("naaaaaaaaa")
        context = {
            'form': form
        }
        return render(request, 'login.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context)
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'signup.html', context)


def log_out(request):
    logout(request)
    return redirect('login')
