from django.shortcuts import render,redirect
from home.models import Task
from django.contrib.auth import authenticate, login as loginUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def home(request):
    context = {'success':False}
    if request.method == "POST":
        title = request.POST['title']
        desc = request.POST['desc']

        ins = Task(taskname = title, taskdesc = desc )
        ins.save()
        context = {'success':True,}
  
    return render(request,'index.html',context)

def tasks(request):   
    alltasks = Task.objects.all()
    print(alltasks)
    context = {'tasks': alltasks}
    return render(request,'tasks.html',context)  

def delete(request,id ):
    alltasks = Task.objects.all() 
    print(id)
    Task.objects.get(pk = id).delete()   
    context = {'success':True,'tasks':alltasks}
    return render(request,'tasks.html',context)        

def update(request, id):
    obj = Task.objects.get(pk = id)
    myobj = {
        "title" : obj.taskname,
        "desc" : obj.taskdesc,
        "id" : obj.id
    }
    return render(request,'update.html',context=myobj)

def edit(request, id):
    obj = Task(pk = id)
    
    obj.title = request.GET['title']
    obj.desc = request.GET['desc']
    import datetime
    update_at = datetime.datetime.now()
    obj.time =  update_at
    inses = Task(taskname = obj.title, taskdesc = obj.desc )
    inses.save()
    Task.objects.get(pk = id).delete()  
       
    alltasks = Task.objects.all()   
    context = {'tasks':alltasks}
    return render(request,'tasks.html',context)

def search(request):  
    if request.method == 'GET':
        search = request.GET['q'] 
        alltasks = Task.objects.all().filter(taskname=search)
        print(alltasks)
        context = {'tasks': alltasks}
        return render(request,'tasks.html',context)  

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        context = {'form':form }
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            user = authenticate(username = username, password = password)
            print(user)
            if user is not None:
                loginUser(request, user)
                return redirect('home' ) 
        else:
            return render(request, 'login.html',context)    

    else:
        form = AuthenticationForm()
        print("naaaaaaaaa")
        context = {
           'form':form
        }
        return render(request, 'login.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')    
        else:
            return render(request, 'signup.html',context)    
    else:
        form = UserCreationForm()
        context = {'form':form}
        return render(request,'signup.html', context)