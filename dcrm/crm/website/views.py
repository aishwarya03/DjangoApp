from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.
def home(request):
    return render(request,'enter.html',{})

def login_user(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #Authenicate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in successfully")
            return redirect('login')
        else:
            messages.success(request,"Please try again beccause there is an error in login credentials.")
            return redirect('login')
    else:
        return render(request,'login.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return render(request,'enter.html',{})

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(username=username,password=password1)
            login(request,user)
            messages.success(request,'You have been successfully registered, welcome')
            return redirect('login')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})