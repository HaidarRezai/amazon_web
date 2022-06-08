from ast import And
from functools import cache
from re import T
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from amazon.models import *
from django.contrib import messages
from amazon.views import profile_update
from django.core.paginator import Paginator
from django.db.models import F, Sum, Avg,Count
from datetime import datetime
from amazon.views_student import all_student
import math
from django.db.models import Q

@login_required(login_url='/')
def home(request):
    if request.user.user_type == '1':
        all_student = Student.objects.filter(timestamp__month = datetime.now().month).count()
        all_teacher = Teacher.objects.all()
        all_class = Group.objects.all()
        all_group = Groups_students.objects.all().count()
        fees_report = Fees.objects.all().order_by('id').reverse()

        paginator = Paginator(fees_report, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        fees_report = paginator.get_page(page_number)

        report_student = Student.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).count()
        report_register = Groups_students.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).count()

        report_fees = Fees.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).count()
        # fees_day = report_fees.aggregate(total=Sum(F('fees')))
        
        prese_teacher = all_teacher.filter(timestamp__year = datetime.now().year).count()
        all_teacher = all_teacher.count()

        prese_class = all_class.filter(timestamp__month = datetime.now().month,).count()
        all_class = all_class.count()
        try:
            prese_fees = (report_fees*100)/report_fees
            presentage = (report_student*100)/all_student
            prese_group = (report_register*100)/all_group
            prese_teacher = (prese_teacher*100)/all_teacher
            prese_class = (prese_class*100)/all_class
        except:
            prese_group = 0
            prese_fees = 0
            presentage = 0
            prese_teacher = 0
            prese_class = 0
            
        info_class = Group.objects.all().order_by('id').reverse()

        paginator = Paginator(info_class, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        info_class = paginator.get_page(page_number)
    
        dic={
            "prese_group":math.floor(prese_group),
            "fees_report":fees_report,
            "prese_fees":math.floor(prese_fees),
            "presentage":math.floor(presentage),
            "prese_teacher":math.floor(prese_teacher),
            "prese_class":math.floor(prese_class),
            "report_fees":report_fees,
            "report_register":report_register,
            "report_student":report_student,
            "all_student":all_student,
            "all_class":all_class,
            "all_teacher":all_teacher,
            "info_class":info_class,
        }
        return render(request,'home.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def teacher_add(request):
    if request.user.user_type == '1':
        return render(request, 'teacher/add_teacher.html')
    else:
        return render(request,'login_page.html')
@login_required(login_url='/')
def teacher_save(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            father_name = request.POST.get('father_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            phone_tow = request.POST.get('phone_tow')
            degree_edu = request.POST.get('degree_edu')
            idcord = request.POST.get('idcord')
            level = request.POST.get('level')
            address_one = request.POST.get('address_one')
            address_tow = request.POST.get('address_tow')
            profile_pic = request.FILES.get('profile_pic')
            
            if CustomUser.objects.filter(email = email).exists():
                messages.warning(request,"Email is Already Taken")
                return redirect('teacher-save')
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request,"Username is Already Taken")
                return redirect('teacher-save')
            else:
                user = CustomUser(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    profile_pic = profile_pic,
                    user_type = 4,
                )
                user.set_password(password)
                user.save()

                teacher = Teacher(
                    admin = user,
                    father_name = father_name,
                    phone_one = phone,
                    phone_tow = phone_tow,
                    degree_edu = degree_edu,
                    address_one = address_one,
                    address_tow = address_tow,
                    idcord = idcord,
                    level = level,
                )
                teacher.save()
                messages.success(request,user.first_name + " " + user.last_name + ' Teacher Successfully Save')
                return redirect('teacher-all')

        return render(request, 'teacher/add_teacher.html')
    else:
        return render(request,'login_page.html')
@login_required(login_url='/')
def teacher_all(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            search = request.POST['search']
            multi = Q(Q(id__icontains=search)|Q(admin__first_name=search)
            |Q(phone_one=search)
            )
            teacher = Teacher.objects.filter(multi)
            dic={
                'teacher':teacher,
                }
        else:
            teacher = Teacher.objects.all().order_by('id').reverse()
            paginator = Paginator(teacher, 8) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            teacher = paginator.get_page(page_number)

            dic={
                'teacher':teacher,
            }
        return render(request,'teacher/teacher_all.html',dic)
    else:
        return render(request,'login_page.html')
def teacher_profile(request,pk):
    if request.user.user_type == '1':
        teacher = Teacher.objects.get(id = pk)
        
        group_teacher = Groups_teachers.objects.filter(
            id_teacher = pk,
            ).order_by('id').reverse()

        am_cl = group_teacher.count()

        ac_cl = group_teacher.aggregate(total=Sum(F('id_group__active')))
        
        paginator = Paginator(group_teacher, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        group_teacher = paginator.get_page(page_number)

        # group = Group.objects.filter(
        #     teacher_one = pk,
        #     ).order_by('id').reverse()

        # paginator = Paginator(group, 8) # Show 25 contacts per page.
        # page_number = request.GET.get('page')
        # group = paginator.get_page(page_number)
        
        dic={
            "teacher":teacher,
            # "group":group,
            "group_teacher":group_teacher,
            "class":am_cl,
            "active":ac_cl['total'],
        }
        return render(request,'teacher/profile.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def teacher_update(request,pk):
    if request.user.user_type == '1':
        teacher = Teacher.objects.filter(id=pk)

        dic={
            "teacher":teacher
        }
        return render(request,'teacher/update_teacher.html',dic)
    else:
        return render(request,'login_page.html')
@login_required(login_url='/')
def teacher_doupdate(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            father_name = request.POST.get('father_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            phone_tow = request.POST.get('phone_tow')
            degree_edu = request.POST.get('degree_edu')
            idcord = request.POST.get('idcord')
            level = request.POST.get('level')
            address_one = request.POST.get('address_one')
            address_tow = request.POST.get('address_tow')
            teacher_id = request.POST.get('teacher_id')
            profile_pic = request.FILES.get('profile_pic')
            
            user = CustomUser.objects.get(id = teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            url ="teacher_profile/{}/".format(user.teacher.id)

            if password !=None and password != "":
                user.set_password(password)
            if profile_pic !=None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()

            teacher = Teacher.objects.get(admin = teacher_id)
            teacher.father_name = father_name
            teacher.phone_one = phone
            teacher.phone_tow = phone_tow
            if degree_edu !=None and degree_edu != "None":
                teacher.degree_edu = degree_edu
            teacher.address_one = address_one
            teacher.address_tow = address_tow
            teacher.idcord = idcord
            if level !=None and level != "None":
                teacher.level = level
            teacher.save()
            messages.success(request,'Record Are Successfully upated')
            return HttpResponseRedirect(url)
        return render(request,'teacher/update_teacher.html')
    else:
        return render(request,'login_page.html')
@login_required(login_url='/')
def teacher_delete(request,pk):
    if request.user.user_type == '1':    
        teacher = Teacher.objects.get(id = pk)
        dic={
            "teacher":teacher,
        }
        return render(request,'teacher/delete.html',dic)
    else:
        return render(request,'login_page.html')   
@login_required(login_url='/')
def teacher_dodelete(request,pk):
    if request.user.user_type == '1':
        teacher = Teacher.objects.get(id = pk)

        teacher.delete()
        messages.success(request,'Record Are Successfully Delete')
        return redirect('teacher-all')
    else:
        return render(request,'login_page.html')
#pay Salary
@login_required(login_url='/')
def pay_salary(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            salary = int(request.POST.get('salary'))
            # baqiyat = request.POST.get('baqiyat')
            group = request.POST.get('group')
            by = CustomUser.objects.get(id = request.user.id)
            group = Groups_teachers.objects.get(id = group)
            teacher = Teacher.objects.get(admin = group.id_teacher.admin)
            url = "teacher_profile/{}/".format(group.id_teacher.id)
            # --------------------------------------------------------------
            teacher.amount_salary += salary
            teacher.save()
            
            salary = Pay( 
                group_teacher = group,
                salary = salary,
                # baqiyat = 0,
                active = 0,
                by = by,
            )
            try:
                salary.save()
                messages.success(request,'Salary is Successfully Pay')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Some Problem try again')
                return HttpResponseRedirect(url)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def payment(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            salary = int(request.POST.get('salary'))
            # baqiyat = request.POST.get('baqiyat')
            teacher = request.POST.get('teacher')

            by = CustomUser.objects.get(id = request.user.id)

            teacher = Teacher.objects.get(id = teacher)
            
            url = "teacher_profile/{}/".format(teacher)
            # --------------------------------------------------------------
            teacher.amount_salary -= salary
            teacher.save()

            payment = Payment(
                teacher = teacher,
                amount = salary,
                by = by,
            )
            payment.save()

            salary = Output( 
                datils = 'Salary paid for teacher',
                money = salary,
                by = by,
            )
            try:
                salary.save()
                messages.success(request,'Salary is Successfully Pay')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Some Problem try again')
                return HttpResponseRedirect(url)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def show_payment(request, pk):
    if request.user.user_type == '1':
        
        payment = Payment.objects.filter(teacher = pk).order_by('id').reverse()
        total_pay = payment.aggregate(total=Sum(F('amount')))
        paginator = Paginator(payment,12) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        payment = paginator.get_page(page_number)

        dic = {
            'payment':payment,
            'total_pay':total_pay['total'],
            'teacher':Teacher.objects.get(id = pk),
        }
        return render(request,'teacher/payment.html',dic)

# @login_required(login_url='/')
# def pay_baqi(request):
#     if request.user.user_type == '1':
#         salary = int(request.POST.get('salary'))
#         group = request.POST.get('group')
        
#         baqi = Pay.objects.get(id = group)
#         by = CustomUser.objects.get(id = request.user.id)
#         url = "show_salary/{}/".format(baqi.group_teacher.id_teacher.id)
        
#         baqi.salary += salary
#         baqi.baqiyat -= salary
#         baqi.by = by
#         baqi.save()
#         output = Output(
#             datils = 'Pay Remainder For Teacher',
#             money = salary,
#             by = by,
#         )
#         output.save()
#         messages.success(request,'Baqi is Successfully Pay')
#         return HttpResponseRedirect(url)
#     else:
#         return render(request,'login_page.html')

@login_required(login_url='/')
def show_salary(request,pk):
    if request.user.user_type == '1':
        group = Groups_teachers.objects.filter(
            id_teacher = pk,
            ).order_by('id').reverse()
        
        teacher = Teacher.objects.get(id = pk) 
        
        paginator = Paginator(group,12) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        group = paginator.get_page(page_number)

        dic={
            "group":group,
             "teacher":teacher,
        }
        return render(request,'teacher/show_salary.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def more_salary(request,pk,id_tea):
    if request.user.user_type == '1':
        gro_tea = Groups_teachers.objects.get(id = pk)

        gro_stu = Groups_students.objects.filter(id_group = id_tea)

        fees_class = gro_stu.aggregate(total=Sum(F('fees__fees')))
        total = fees_class['total']
        if gro_tea.amount_salary.type_salary == 'Percentage':
            if gro_tea.include == '2':
                salary = ((gro_tea.amount_salary.salary * total)/100)/2
            else:
                salary = (gro_tea.amount_salary.salary * total)/100
        elif gro_tea.amount_salary.type_salary == 'Fixed':
            salary = gro_tea.amount_salary.salary
        # -------------------------------------------------------------------------
        dic = {
            "gro_tea":gro_tea,
            "fees_class":total,
            "salary":int(salary),
        }
        
        return render(request,'teacher/more_salary.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def pay_month(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            salary = int(request.POST.get('salary'))
            # baqiyat = request.POST.get('baqiyat')
            teacher = request.POST.get('teacher')
            by = CustomUser.objects.get(id = request.user.id)
            url = "list_payed/{}/".format(teacher)
            teacher = Teacher.objects.get(id = teacher)
            # -------------------------------------------------
            teacher.amount_salary += salary
            teacher.save()
            
            salary = Pay_month( 
                teacher = teacher,
                salary = salary,
                baqiyat = 0,
                by = by,
            )
            try:
                salary.save()
                messages.success(request,'Salary is Successfully Pay')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Some Problem try again')
                return HttpResponseRedirect(url)
    else:
        return render(request,'login_page.html')

# def show_remaind_month(request,pk):
#     baqi = Pay_month.objects.get(id = pk)
#     dic = {
#         'baqi':baqi,
#     }
#     return render(request,'teacher/pay_remaid_month.html',dic)

# def pay_remaind_month(request):
#     if request.user.user_type == '1':
#         salary = int(request.POST.get('salary'))
#         id_pay = request.POST.get('id_pay')

#         url = "show_remaind_month/{}/".format(id_pay)

#         by = CustomUser.objects.get(id = request.user.id)
#         baqi = Pay_month.objects.get(id = id_pay)
       
       
#         baqi.salary += salary
#         baqi.baqiyat -= salary
#         baqi.by = by
#         baqi.save()
#         output = Output(
#             datils = 'Pay Remainder For Teacher',
#             money = salary,
#             by = by,
#         )
#         output.save()
#         messages.success(request,'Baqi is Successfully Pay')
#         return HttpResponseRedirect(url)
#     else:
#         messages.warning(request,'Some Problem try again')
#         return render(request,'login_page.html')
@login_required(login_url='/')
def list_payed(request,pk):
    if request.user.user_type == '1':
        pay_month = Pay_month.objects.filter(
            teacher = pk,
            ).order_by('id').reverse()

        teacher = Teacher.objects.get(id = pk) 

        paginator = Paginator(pay_month,18) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        pay_month = paginator.get_page(page_number)

        dic = {
            'pay_month':pay_month,
            'teacher':teacher,
        }
        
        return render(request,'teacher/pay_list.html',dic)
    else:
        return render(request,'login_page.html')

# def update_salary(request):
#     if request.method == "POST":
#         salary = request.POST.get('salary')
#         baqiyat = request.POST.get('baqiyat')
#         pish_pay = request.POST.get('pish_pay')
#         group = request.POST.get('group')

#         try:
#             salarys = Salary_one.objects.get(group = group)
#             salarys.salary = salary
#             salarys.baqiyat = baqiyat
#             salarys.pish_pay = pish_pay
        
#             salarys.save()
#             messages.success(request,'Salary is Successfully Update')
#             return redirect('teacher-all')
#         except:
#             messages.warning(request,'Salary is dond have payed')
#             return redirect('teacher-all')

#     return render(request,'teacher/show_salary.html')


# @login_required(login_url='/')
# def teacher(request):
#     return render(request,'teacher/teacher.html')