from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,Group
from .decorators import *
from django.contrib.auth.decorators import login_required


# Create your views here.



@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def userhome(request):
    return render(request,'base/userhome.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminhome(request):
    return render(request,'base/adminhome.html')



def loginUser(request):
    if request.method=="POST":
        print("hello")
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if(not username or not password):
            messages.error(request, "Please fill all details")
            return redirect('login')
       
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group == 'admin':
                return redirect('adminhome')
            return redirect('userhome')
        else:
            messages.info(request,"Username or password is incorrect")
            return redirect('login')
        
    return render(request,"base/login.html")





def signup(request):
    if request.method == 'POST':
        mis=request.POST.get('misno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if(not email or not password ):
            messages.error(request, "Please fill all details")
            return render(request, 'base/signup.html')
        elif( len(password) < 8 or not any(char.isupper() for char in password) or  not any(char.isdigit() for char in password) or not any(char in '!@#$%^&*()-_=+[{]};:|,<.>/?' for char in password)):
            messages.error(request, "Password must contain at least 8 characters, including one uppercase letter, one digit, and one special character.")
            print("checkpoint")
            return render(request, 'base/signup.html')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, "User with this email already exists.")
                return render(request, 'base/signup.html')
            if password != password2:
                messages.error(request, "Password doesn't match")
                return render(request, 'base/signup.html')
            # Create the user manually
            user = User.objects.create_user(username=mis,email=email, password=password)
            group=Group.objects.get(name='user')
            user.groups.add(group)
        
           
           
            user.save()
            return redirect('login')
    
    return render(request,"base/signup.html")


def logoutUser(request):
    logout(request)
    return redirect('login')