from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout,authenticate
from .forms import TodoForm
from .models import todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'todo/home.html')
def signupuser(request):
    if request.method =='GET':

        return render(request,'todo/signup.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentuser')
            except IntegrityError:
                return render(request,'todo/signup.html',{'form':UserCreationForm(),"error":'Username already Taken'})
        else:
            return render(request,'todo/signup.html',{'form':UserCreationForm(),"error":'Password Didnt Match'})
@login_required
def currentuser(request):
    todos=todo.objects.filter(user=request.user,Datecompleted__isnull=True)


    return render(request,'todo/currentuser.html',{"todos":todos})
@login_required
def completed(request):
    todos=todo.objects.filter(user=request.user,Datecompleted__isnull=False).order_by('-Datecompleted')


    return render(request,'todo/completed.html',{"todos":todos})



def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method=='GET':
        return render(request,'todo/login.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/login.html',{'form':AuthenticationForm(),"error":'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('currentuser')
@login_required
def todoos(request):
    if request.method=='GET':
        return render(request,'todo/todo.html',{'form':TodoForm()})
    else:
        try:
            form=TodoForm(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user = request.user
            form.save()
            return redirect('currentuser')

        except  ValueError:
                return render(request,'todo/todo.html',{'form':TodoForm(),"error":'Bad Details Please Try Again'})
@login_required
def updatetodo(request,todo_pk):
    todowo=get_object_or_404(todo,pk=todo_pk,user=request.user)
    form=TodoForm(instance=todowo)
    if request.method=='GET':
        return render(request,'todo/updatetodo.html',{"todowo":todowo,"form":form})
    else:
        try:
            form=TodoForm(request.POST,instance=todowo)
            form.save()
            return redirect('currentuser')
        except  ValueError:
                return render(request,'todo/updatetodo.html',{"todowo":todowo,"form":form ,"error":'Bad Details Please Try Again'})
@login_required
def completetodo(request,todo_pk):
    todowo=get_object_or_404(todo,pk=todo_pk,user=request.user)
    if request.method=="POST":
        todowo.Datecompleted=timezone.now()
        todowo.save()
        return redirect('currentuser')
@login_required
def deletetodo(request,todo_pk):
    todowo=get_object_or_404(todo,pk=todo_pk,user=request.user)
    if request.method=="POST":
        todowo.Datecompleted=timezone.now()
        todowo.delete()
        return redirect('currentuser')
