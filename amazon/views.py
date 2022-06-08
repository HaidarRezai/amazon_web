import re
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from amazon.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Avg,Count
from django.core.paginator import Paginator
from amazon.models import *
# Create your views here.

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
                return redirect('oner')
            elif user_type == '3':
                return HttpResponse('This is Student panel')
            elif user_type == '4':
                return redirect('teacher-system')
            else:
                messages.error(request,'Email and password are Invalid')
                return redirect('login')
        else:
            messages.error(request,'Email and password are Invalid')
            return redirect('login')
    
def doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        return render(request,'profile.html')
    else:
        logout(request)
        return render(request,'login_page.html')
@login_required(login_url='/')
def profile_update(request):
    if request.user.user_type == '1':
        user = CustomUser.objects.get(id = request.user.id)
        dic={
            "user":user
        }
        return render(request,'profile_upate.html',dic)
    if request.user.user_type == '4':
        user = CustomUser.objects.get(teacher__admin = request.user.id)
        print(user)
        dic={
            "user":user
        }
        return render(request,'teacher_system/profile_upate.html',dic)
    else:
        return render(request,'login_page.html')
@login_required(login_url='/')
def doprofile_update(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            # username = request.POST.get('username')
            # email = request.POST.get('email')
            password = request.POST.get('password')
            profile_pic = request.FILES.get('profile_pic')

            try:
                customuser = CustomUser.objects.get(id = request.user.id)

                customuser.first_name = first_name
                customuser.last_name = last_name

                if password !=None and password != "":
                    customuser.set_password(password)
                if profile_pic !=None and profile_pic != "":
                    customuser.profile_pic = profile_pic
                customuser.save()
                messages.success(request,'Your Profile Update successfully')
                redirect('profile-update')
            except:
                messages.success(request,'Your Profile Update Faild')

        return render(request,'profile_upate.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def qars(request):
    if request.user.user_type  == '1' or '2':
        fees = Fees.objects.all()
        amount = fees.aggregate(total=Sum(F('baqi')))

        
        dic = {
            'fees':fees,
            'amount':amount['total'],
        }
        return render(request,'qars/qars.html',dic)
    else:
        return render(request,'login_page.html')
def input_add(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            money = request.POST.get('money')
            datils = request.POST.get('datils')
            input = Input(
                datils = datils,
                money = money,
                by = CustomUser.objects.get(id = request.user.id),
            )
            input.save()
            messages.success(request,'Money is Successfully Saved')
            return redirect('acounting')
        else:
            messages.warning(request,'Some Problem try again')
            return redirect('acounting')
    else:
        return render(request,'login_page.html')
def output_add(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            money = request.POST.get('money')
            datils = request.POST.get('datils')
            output = Output(
                datils = datils,
                money = money,
                by = CustomUser.objects.get(id = request.user.id),
            )
            output.save()
            messages.success(request,'Money is Successfully Payed')
            return redirect('acounting')
        else:
            messages.warning(request,'Some Problem try again')
            return redirect('acounting')
    else:
        return render(request,'login_page.html')

def about_us(request):
    return render(request,'about_us.html')