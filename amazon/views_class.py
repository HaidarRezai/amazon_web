from ast import For, Not
from asyncio.windows_events import NULL
from email import message
from tokenize import group
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from amazon.models import *
from django.contrib import messages
import calendar
from django.core.paginator import Paginator
from datetime import datetime
import io
from django.contrib.auth.decorators import login_required
from.forms import *
from django.db.models import F, Sum, Avg,Count

@login_required(login_url='/')
def class_add(request):
    if request.user.user_type == '1':

        info_class = Group.objects.filter( 
        active = '1',
        ).order_by('id').reverse()
    

        dodeactive = Group.objects.filter(
            end_date__year = datetime.now().year, 
            end_date__month = datetime.now().month,
            end_date__day = datetime.now().day,
        )
        for i in dodeactive:
            i.active = 0
            i.save()

        paginator = Paginator(info_class, 20) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        info_class = paginator.get_page(page_number)

        dic={
            "info_class":info_class,
            "teacher": Teacher.objects.filter(active = '1')
        }
        return render(request,'class/add_class.html',dic)
    else:
        return render(request,'login_page.html')
    

@login_required(login_url='/')
def show_all(request):
    if request.user.user_type == '1':
        info_class = Group.objects.filter(
            active = '0',
        ).order_by('id').reverse()

        paginator = Paginator(info_class, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        info_class = paginator.get_page(page_number)
        
        dic={
            "info_class":info_class,
            "teacher": Teacher.objects.filter(active = '1'),
        }
        return render(request,'class/add_class.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_save(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            subject = request.POST.get('subject')
            number_class = request.POST.get('number_class')
            start_time = request.POST.get('start_time')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            fees = request.POST.get('fees')

            teacher_one = request.POST.get('teacher_one')
            type_salary_one = request.POST.get('type_salary_one')
            salary_one = request.POST.get('salary_one')
            
            teacher_tow = request.POST.get('teacher_tow')
            type_salary_tow = request.POST.get('type_salary_tow')
            salary_tow = request.POST.get('salary_tow')

            if teacher_one == 'Null':
                messages.warning(request,'Group Filed Added')
                return redirect('class-add')
            else:
                if teacher_tow != 'Null':
                    include = '2'
                else:
                    include = '1'
                teacher_one = Teacher.objects.get(id = teacher_one)

                group = Group(
                    subject = subject,
                    number_class = number_class,
                    start_time = start_time,
                    start_date = start_date,
                    end_date = end_date,
                    fees = fees, 
                )
                group.save()

                g_t_one = Groups_teachers(
                    id_teacher = teacher_one,
                    id_group = group,
                    position_teacher = 'one',
                    include = include,
                )
                g_t_one.save()

                am_one = Amount_salary(
                    group_teacher = g_t_one,
                    type_salary = type_salary_one,
                    salary = salary_one,
                )
                am_one.save()
            # -----------------------------------------------------

                if teacher_tow != 'Null':
                        
                    teacher_tow = Teacher.objects.get(id = teacher_tow)

                    g_t_tow = Groups_teachers(
                        id_teacher = teacher_tow,
                        id_group = group,
                        position_teacher = 'tow',
                        include = include,
                    )
                    g_t_tow.save()

                    am_tow = Amount_salary(
                        group_teacher = g_t_tow,
                        type_salary = type_salary_tow,
                        salary = salary_tow,
                    )
                    am_tow.save()
                else:
                    messages.success(request,'Group Successfully Added')

                messages.success(request,'Group Successfully Added')
                return redirect('class-add')
           
                # messages.warning(request,'Group Filed Added')
                # return redirect('class-add')
            
        return render(request,'class/add_class.html')
    else:
        return render(request,'login_page.html')

#.......................
@login_required(login_url='/')
def class_update(request,pk):
    if request.user.user_type == '1':
        group = Group.objects.get(id = pk)
        
        group_teacher = Groups_teachers.objects.filter(id_group = pk)

        teacher = Teacher.objects.filter(active = '1')
    
        dic={
            "group":group,
            "teacher":teacher,
            "group_teacher":group_teacher,
            
        }
        return render(request,'class/update_class.html',dic)
    else:
        return render(request,'login_page.html')
#.....................
@login_required(login_url='/')
def class_delete(request,pk):
    if request.user.user_type == '1':
        group = Group.objects.get(id = pk)
        dic={
            "group":group
        }
        return render(request,'class/Delete.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_doupdate(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            id_class = request.POST.get('id_class')
            subject = request.POST.get('subject')
            number_class = request.POST.get('number_class')
            start_time = request.POST.get('start_time')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            fees = request.POST.get('fees')
            teacher_one = request.POST.get('teacher_one')
            teacher_tow = request.POST.get('teacher_tow')

            type_salary_one = request.POST.get('type_salary_one')
            id_teacher_one = request.POST.get('id_teacher_one')
            salary_one = request.POST.get('salary_one')
            id_amount_one = request.POST.get('id_amount_one')

            type_salary_tow = request.POST.get('type_salary_tow')
            salary_tow = request.POST.get('salary_tow')
            id_teacher_tow = request.POST.get('id_teacher_tow')
            id_amount_tow = request.POST.get('id_amount_tow')
        
            
            class_update = Group.objects.get(id = id_class)

            class_update.subject = subject
            class_update.number_class = number_class

            if start_time !=None and start_time != "":
                class_update.start_time = start_time

            if start_date !=None and start_date != "":
                class_update.start_date = start_date

            if end_date !=None and end_date != "":
                class_update.end_date = end_date

            class_update.fees = fees

            class_update.save()
            
            if teacher_one != None and teacher_one != "":
                teacher_one = Teacher.objects.get(id = teacher_one)

                g_t_one = Groups_teachers.objects.get(id = id_teacher_one)
                g_t_one.id_teacher = teacher_one
                # g_t_one.id_group = class_update
                g_t_one.position_teacher = 'one'
                g_t_one.save()

            am_one = Amount_salary.objects.get(id = id_amount_one)
            # am_one.group_teacher = g_t_one
            am_one.type_salary = type_salary_one
            am_one.salary = salary_one
            am_one.save()
            
            if teacher_tow != None and teacher_tow != "":
                teacher_tow = Teacher.objects.get(id = teacher_tow)

                g_t_tow = Groups_teachers.objects.get(id = id_teacher_tow)
                g_t_tow.id_teacher = teacher_tow
                # g_t_tow.class_update = class_update
                g_t_tow.position_teacher = 'tow'
                g_t_tow.save()
            try:
                am_tow = Amount_salary.objects.get(id = id_amount_tow)
                # am_tow.group_teacher = g_t_tow
                am_tow.type_salary = type_salary_tow
                am_tow.salary = salary_tow
                am_tow.save()
            except:
                messages.success(request,'Record Are Successfully upated')

            messages.success(request,'Record Are Successfully upated')
            return redirect('class-add')
        return render(request,'class/update_class.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')    
def doclass_delete(request,pk):
    if request.user.user_type == '1':
        group = Group.objects.get(id = pk)

        group.delete()

        messages.success(request,'Group Successfully Delete')
        return redirect('class-add')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_score(request,pk):
    if request.user.user_type == '1' or request.user.user_type == '4':
        students = Groups_students.objects.filter(id_group = pk)
        paginator = Paginator(students, 1) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        students = paginator.get_page(page_number)

        group = Group.objects.get(id = pk)
        dic={
            "students":students,
            "group":group,
        }
        return render(request,'class/set_score.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_resultcart(request,pk):
    if request.user.user_type == '1' or request.user.user_type == '4':
        students = Groups_students.objects.filter(id_group = pk)
        group = Group.objects.get(id = pk)
        teacher = Groups_teachers.objects.filter(id_group = pk)

        paginator = Paginator(students, 1) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        students = paginator.get_page(page_number)
        
        dic={
            "students":students,
            "group":group,
            "teacher":teacher,
        }
        return render(request,'class/resultcart.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_report(request,pk):
    if request.user.user_type == '1' or request.user.user_type == '4':
        students = Groups_students.objects.filter(id_group = pk)
        group = Group.objects.get(id = pk)
        teacher = Groups_teachers.objects.filter(id_group = pk)

        dic={
            "students":students,
            "group":group,
            "teacher":teacher,
        }
        return render(request,'class/report.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_info(request,pk):
    if request.user.user_type == '1':
        students = Groups_students.objects.filter(id_group = pk)
        teachers = Groups_teachers.objects.filter(id_group = pk)
        fees_a = students.aggregate(total=Sum(F('fees__fees')))
        group = Group.objects.get(id = pk)
        dic={
            "students":students,
            "total_fees":fees_a['total'],
            # "total_fees":students.id_group.fees.annotate(
                # total=sum("fees")
                # ),
            "students_count":students.count(),
            "teachers":teachers,
            "group":group,
        }
        return render(request,'class/Haziri.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def present(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            total = int(request.POST.get('total'))
            ur = int(request.POST.get('ur'))
            url ="class_info/{}/".format(ur)
            i = 1
            while i <= total:
                
                pre = request.POST.get('pre'+str(i))
                id = request.POST.get('id'+str(i))
                group_stu = Groups_students.objects.get(id = int(id))
                if pre == None:
                    pre = 0
                
                presen = Present(
                    group_student = group_stu,
                    present = pre,
                )
                presen.save()


                i += 1
            messages.success(request,'Record Are Successfully upated')
            return HttpResponseRedirect(url)
    else:
        return render(request,'login_page.html')

def attendance(request,pk):
    if request.user.user_type == '1':
        present = Present.objects.filter(group_student = pk,
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
        )
        dic = {
            'present':present,
        }
        return render(request,'class/attendance.html',dic)
    else:
        return render(request,'login_page.html')

def attendance_show(request,pk):
    att = Present.objects.filter(group_student__id_group = pk).order_by('timestamp').reverse()
    stu = Groups_students.objects.filter(id_group = pk)

    dic = {
        'att':att,
        'stu':stu,
    }

    return render(request, 'class/attendance_all.html',dic)

def acounting (request):
    if request.user.user_type == '1':
        input = Input.objects.aggregate(total=Sum(F('money')))
        output = Output.objects.aggregate(total=Sum(F('money')))

        report_day = Input.objects.filter( 
            by = request.user.id,
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).order_by('id').reverse()
        totla_report_day = report_day.aggregate(total=Sum(F('money')))

        # .............................
        output_report_day = Output.objects.filter(
            by = request.user.id, 
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            timestamp__day = datetime.now().day,
            ).order_by('id').reverse()
        output_totla_report_day = output_report_day.aggregate(total=Sum(F('money')))


        report_month = Input.objects.filter( 
            by = request.user.id,
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            ).order_by('id').reverse()
        totla_report_month = report_month.aggregate(total=Sum(F('money')))

        # .............................
        output_report_month = Output.objects.filter( 
            by = request.user.id,
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
            ).order_by('id').reverse()
        output_totla_report_month = output_report_month.aggregate(total=Sum(F('money')))

        report_year = Input.objects.filter( 
            by = request.user.id,
            timestamp__year = datetime.now().year,
            ).order_by('id').reverse()
        totla_report_year = report_year.aggregate(total=Sum(F('money')))

        # .............................
        output_report_year = Output.objects.filter( 
            by = request.user.id,
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
            by = request.user.id,
            timestamp__year = search_date[:4],
            timestamp__month = search_date[5:],
            ).order_by('id').reverse()
            totla_report_day = report_day.aggregate(total=Sum(F('money')))
            # .............................
            output_report_day = Output.objects.filter( 
                by = request.user.id,
                 timestamp__year = search_date[:4],
                timestamp__month = search_date[5:],
                ).order_by('id').reverse()
            output_totla_report_day = output_report_day.aggregate(total=Sum(F('money')))

        
        try:
            if output_totla_report_day['total'] == None:
                totla_day = 0
            else:
                totla_day = (totla_report_day['total'])-(output_totla_report_day['total'])
            totla_month = (totla_report_month['total'])-(output_totla_report_month['total'])
            totla_year = (totla_report_year['total'])-(output_totla_report_year['total'])
        except:
            totla_day = 0
            totla_month = 0
            totla_year = 0

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
            
            'totla_day':totla_day,
            'totla_month':totla_month,
            'totla_year':totla_year,

            'input':input['total'],
            'output':output['total'],

        }
        return render(request,'admin/accounting.html',dic)
    else:
        return render(request,'login_page.html')

def finisht(request):
    if request.method == "POST":
        id = request.POST.get('id_class')

        group = Group.objects.get(id = id)
        if group.active == '1':
            group.active = 0
            mess ='Class Successfully Deactive'
        else:
            group.active = 1
            mess ='Class Successfully Active'
        group.save()
        messages.success(request,mess)
        return redirect('class-add')