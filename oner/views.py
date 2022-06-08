from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from amazon.models import *
from django.contrib import messages
from django.core.paginator import Paginator
import math
from django.db.models import F, Sum, Avg,Count
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

@login_required(login_url='/')
def oner(request):
    if request.user.user_type == '2':
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
        return render(request,'oner/home.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def staff_add(request):
    if request.user.user_type == '2':
        return render(request, 'oner/staff_add.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def staff_save(request):
    if request.user.user_type == '2':
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
            address_one = request.POST.get('address_one')
            address_tow = request.POST.get('address_tow')
            profile_pic = request.FILES.get('profile_pic')
                
            if CustomUser.objects.filter(email = email).exists():
                messages.warning(request,"Email is Already Taken")
                return redirect('staff-add')
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request,"Username is Already Taken")
                return redirect('staff-add')
            else:
                user = CustomUser(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    profile_pic = profile_pic,
                    user_type = 1,
                )
                user.set_password(password)
                user.save()

                staff = Staff(
                    admin = user,
                    father_name = father_name,
                    phone_one = phone,
                    phone_tow = phone_tow,
                    degree_edu = degree_edu,
                    address_one = address_one,
                    address_tow = address_tow,
                    idcord = idcord,
                )
                staff.save()
                messages.success(request,user.first_name + " " + user.last_name + ' Staff Successfully Save')
                return redirect('staff-add')
        return render(request, 'oner/staff_add.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def staff_all(request):
    if request.user.user_type == '2':
        staff = Staff.objects.all()
        if request.method == "POST":
                search = request.POST['search']
                multi = Q(Q(admin__id__icontains=search)|
                Q(admin__first_name__icontains=search)|
                Q(admin__last_name__icontains=search)
                |Q(phone_one__icontains=search)
                )
                staff = Staff.objects.filter(multi)
                dic={
                    'staff':staff,
                    }
        paginator = Paginator(staff, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        staff = paginator.get_page(page_number)
            
        dic = {
            'staff':staff,
        }
        return render(request, 'oner/staff_view.html',dic)
    else:
        return render(request,'login_page.html') 
@login_required(login_url='/')
def acounting (request):
    if request.user.user_type == '2':
        input = Input.objects.aggregate(total=Sum(F('money')))
        output = Output.objects.aggregate(total=Sum(F('money')))
        staff = CustomUser.objects.filter(user_type = '1')

        report_day = Input.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).order_by('id').reverse()
        totla_report_day = report_day.aggregate(total=Sum(F('money')))

        # .............................
        output_report_day = Output.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).order_by('id').reverse()
        output_totla_report_day = output_report_day.aggregate(total=Sum(F('money')))


        report_month = Input.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            ).order_by('id').reverse()
        totla_report_month = report_month.aggregate(total=Sum(F('money')))

        # .............................
        output_report_month = Output.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            ).order_by('id').reverse()
        output_totla_report_month = output_report_month.aggregate(total=Sum(F('money')))

        report_year = Input.objects.filter( 
            timestamp__year = datetime.now().year,
            ).order_by('id').reverse()
        totla_report_year = report_year.aggregate(total=Sum(F('money')))

        # .............................
        output_report_year = Output.objects.filter( 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            ).order_by('id').reverse()
        output_totla_report_year = output_report_year.aggregate(total=Sum(F('money')))



        try:
            pre_report_day = ( 100 * totla_report_day['total'] )/input['total'] 
            pre_report_month = (100* totla_report_month['total'])/input['total']
            pre_report_year = (100* totla_report_year['total'])/input['total']
        except:
            pre_report_day = 0
            pre_report_month = 0
            pre_report_year = 0


        if request.method == "POST":
            search_date = request.POST.get('search')
            report_day = Input.objects.filter( 
            
            timestamp__year = search_date[:4],
            timestamp__month = search_date[5:]
            ).order_by('id').reverse()
            totla_report_day = report_day.aggregate(total=Sum(F('money')))
            # .............................
            output_report_day = Output.objects.filter( 
                
            timestamp__year = search_date[:4],
            timestamp__month = search_date[5:],
                ).order_by('id').reverse()
            output_totla_report_day = output_report_day.aggregate(total=Sum(F('money')))

            

        dic ={
            'report_day':report_day,
            'totla_report_day':totla_report_day['total'],
            'pre_report_day':int(pre_report_day),
            
            'totla_report_month':totla_report_month['total'],
            'pre_report_month':int(pre_report_month),
            'report_year':report_year,
            'totla_report_year':totla_report_year['total'],
            'pre_report_year':int(pre_report_year),

            'output_report_day':output_report_day,
            'output_totla_report_day':output_totla_report_day['total'],
            
            'output_totla_report_month':output_totla_report_month['total'],
            'output_report_year':output_report_year,
            'output_totla_report_year':output_totla_report_year['total'],

            'input':input['total'], 
            'output':output['total'],

            'staff':staff,

        }
        return render(request,'oner/accounting.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def staff_profile(request,pk):
        if request.user.user_type == '2':
            user = CustomUser.objects.get(id   = pk)

            dic={
                "user":user,
            }
            return render(request,'oner/profile.html',dic)
        else:
            return render(request,'login_page.html')

@login_required(login_url='/')
def staff_update(request,pk):
    if request.user.user_type == '2':
        staff = CustomUser.objects.get(id=pk)

        dic={
            "staff":staff,
        }
        return render(request,'oner/update_staff.html',dic)
    else:
        return render(request,'login_page.html')


@login_required(login_url='/')
def staff_doupdate(request):
    if request.user.user_type == '2':
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
            address_one = request.POST.get('address_one')
            address_tow = request.POST.get('address_tow')
            staff_id = request.POST.get('staff_id')
            profile_pic = request.FILES.get('profile_pic')
            
            user = CustomUser.objects.get(id = staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            url ="/oner/staff_update/{}/".format(staff_id)

            if password !=None and password != "":
                user.set_password(password)
            if profile_pic !=None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()

            staff = Staff.objects.get(admin = staff_id)
            staff.father_name = father_name
            staff.phone_one = phone
            staff.phone_tow = phone_tow
            staff.degree_edu = degree_edu
            staff.address_one = address_one
            staff.address_tow = address_tow
            staff.idcord = idcord
            staff.save()
            messages.success(request,'Record Are Successfully upated')
            return HttpResponseRedirect(url)
        return render(request,'teacher/update_teacher.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def staff_delete(request,pk):
    if request.user.user_type == '2':    
        user = CustomUser.objects.get(id = pk)
        dic={
            "user":user,
        }
        return render(request,'oner/delete.html',dic)
    else:
        return render(request,'login_page.html') 

@login_required(login_url='/')
def staff_dodelete(request,pk):
    if request.user.user_type == '2':    
        user = Staff.objects.get(admin__id = pk)

        user.delete()
        messages.success(request,'Record Are Successfully Delete')
        return redirect('staff-all')
    else:
        return render(request,'login_page.html') 