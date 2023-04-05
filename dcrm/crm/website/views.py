from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
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

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,'You must login to view that record.')
        return redirect('login')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record Has been deleted successfully")
        return redirect('login')
    else:
        messages.success(request,'You must login to delete that record.')
        return redirect('login')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request,'Record Added.')
                return redirect('login')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,'You must login to add that record.')
        return redirect('login')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record is Updated.')
            return redirect('login')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,'You must login to update that record.')
        return redirect('login')