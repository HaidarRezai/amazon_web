from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def home(request):
    return render(request,'home.html')

    
@login_required(login_url='/')
def teacher(request):
    return render(request,'teacher/teacher.html')