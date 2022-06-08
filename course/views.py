from django.shortcuts import render,redirect,HttpResponse
from course.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'index.html')



def LOGIN(request):
    return render(request,'login_page.html')

def dologin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, 
        username=request.POST.get('email'),
        password=request.POST.get('password'),)

        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('home')
            elif user_type == '2':
                return HttpResponse('This is Staff panel')
            elif user_type == '3':
                return HttpResponse('This is Student panel')
            else:
                messages.error(request,'Email and password are Invalid')
                return redirect('login')
        else:
            messages.error(request,'Email and password are Invalid')
            return redirect('login')

def doLogout(request):
    logout(request)
    return redirect('login')

def PROFILE(request):
    return render(request,'profile.html')

def teacher_update(request):
    return render(request,'update_teacher.html')
