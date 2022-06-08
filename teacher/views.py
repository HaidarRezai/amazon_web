from ast import And
from functools import cache
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

@login_required(login_url='/')
def my_profile(request):
    if request.user.user_type == '4':
        custom_user = CustomUser.objects.get(id = request.user.id)

        group_teacher = Groups_teachers.objects.filter(
            id_teacher = custom_user.teacher.id,
            ).order_by('id').reverse()
        
        paginator = Paginator(group_teacher, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        group_teacher = paginator.get_page(page_number)

        dic = {
            'group_teacher':group_teacher,
            'custom_user':custom_user,
        }
        return render(request,'teacher_system/profile.html',dic)
    return render(request,'login_page.html')

@login_required(login_url='/')
def teacher_update(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            # username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            profile_pic = request.FILES.get('profile_pic')

            try:
                customuser = CustomUser.objects.get(teacher__admin = request.user.id)

                customuser.first_name = first_name
                customuser.last_name = last_name
                customuser.email = email

                if password !=None and password != "":
                    customuser.set_password(password)
                if profile_pic !=None and profile_pic != "":
                    customuser.profile_pic = profile_pic
                customuser.save()
                messages.success(request,'Your Profile Update successfully')
                redirect('my-profile')
            except:
                messages.success(request,'Your Profile Update Faild')

        return redirect('my-profile')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def my_class(request,pk):
    if request.user.user_type == '4':
        students = Groups_students.objects.filter(id_group = pk)
        teachers = Groups_teachers.objects.filter(id_group = pk)
        
        group = Group.objects.get(id = pk)
    
        fees_a = students.aggregate(total=Sum(F('fees__fees')))
    
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
        return render(request,'teacher_system/Haziri.html',dic)
    return render(request,'login_page.html')

@login_required(login_url='/')
def my_student(request,pk):
    if request.user.user_type == '4':
        group_student = Groups_students.objects.get(
            id = pk,
        ) 
        try:
            tot_rea = (group_student.middle_skill.reading)+(group_student.final_skill.reading)
            tot_wri = (group_student.middle_skill.writing)+(group_student.final_skill.writing)
            tot_lis = (group_student.middle_skill.listening)+(group_student.final_skill.listening)
            tot_spe = (group_student.middle_skill.speaking)+(group_student.final_skill.speaking)
            
            tot_all = tot_rea + tot_wri + tot_lis + tot_spe
            if tot_all >= 80:
                result = 'Passed'
            else:
                result = 'Failed'
        except:
            tot_rea = 0
            tot_wri = 0
            tot_lis = 0
            tot_spe = 0
            tot_all = 0
            result = 'Failed'
        try:
            tot_rea_sc = (group_student.score.score)+(group_student.score.final_score)+(group_student.score.activate)+(group_student.score.home_work)
            activate = (group_student.score.activate)+(group_student.score.home_work) 
            if tot_rea_sc >= 60:
                result_s = 'Passed'
            else:
                result_s = 'Failed'
        except:
            tot_rea_sc = 0
            activate = 0
            result_s = 'Failed'

        dic={
            "tot_rea":tot_rea,
            "tot_wri":tot_wri,
            "tot_lis":tot_lis,
            "tot_spe":tot_spe,
            "tot_all":tot_all,
            "result":result,
            "result_s":result_s,
            "group_student":group_student,
            "tot_rea_sc":tot_rea_sc,
            "group_all": Group.objects.all(),
            'activate':activate,
        }
        return render(request,'teacher_system/class_info.html',dic)
    return render(request,'login_page.html')

@login_required(login_url='/')
def set_score_student(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            score = request.POST.get('score')
            final_score = request.POST.get('final_score')
            activate = request.POST.get('activate')
            home_work = request.POST.get('home_work')

            url = "my_student/{}/".format(group_student)

            group_student = Groups_students.objects.get(id = group_student)

            try:
                score = Score(
                    group_student = group_student,
                    score = score,
                    final_score = final_score,
                    activate = activate,
                    home_work = home_work,
                )
                score.save()
                messages.success(request,'Score is Successfully Set')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Score is was Set')
                return redirect('my-profile')
    return render(request,'login_page.html')

@login_required(login_url='/')
def update_score_student(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            score = request.POST.get('score')
            final_score = request.POST.get('final_score')
            activate = request.POST.get('activate')
            home_work = request.POST.get('home_work')

            url = "my_student/{}/".format(group_student)

            score_update = Score.objects.get(group_student = group_student)
            score_update.score = score
            score_update.final_score = final_score
            score_update.activate = activate
            score_update.home_work = home_work
            score_update.save()
            messages.success(request,'Score is Successfully Update')
            return HttpResponseRedirect(url)
    return render(request,'login_page.html')

@login_required(login_url='/')
def middle_skill_student(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "my_student/{}/".format(group_student)

            group_student = Groups_students.objects.get(id = group_student)

            try:
                score = Middle_skill(
                    group_student = group_student,
                    reading = reading,
                    writing = writing,
                    listening = listening,
                    speaking = speaking,
                )
                score.save()
                messages.success(request,'Middle Skill score is Successfully Set')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Middle Skill score is was Set')
                return redirect('my-profile')
    return render(request,'login_page.html')

@login_required(login_url='/')
def upd_mid_ski_student(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "my_student/{}/".format(group_student)

            middle_skill = Middle_skill.objects.get(group_student = group_student)

            middle_skill.reading = reading
            middle_skill.writing = writing
            middle_skill.listening = listening
            middle_skill.speaking = speaking
            middle_skill.save()
            messages.success(request,'Middle Skill Score is Successfully Update')
            return HttpResponseRedirect(url)
    return render(request,'login_page.html')

@login_required(login_url='/')
def final_skill_student(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "my_student/{}/".format(group_student)

            group_student = Groups_students.objects.get(id = group_student)

            try:
                score = Final_skill(
                    group_student = group_student,
                    reading = reading,
                    writing = writing,
                    listening = listening,
                    speaking = speaking,
                )
                score.save()
                messages.success(request,'Final Skill score is Successfully Set')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Fanal Skill score is was Set')
                return HttpResponseRedirect(url)
    return render(request,'login_page.html')

@login_required(login_url='/')
def upd_fin_ski_student(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "my_student/{}/".format(group_student)

            final_skill = Final_skill.objects.get(group_student = group_student)

            final_skill.reading = reading
            final_skill.writing = writing
            final_skill.listening = listening
            final_skill.speaking = speaking
            final_skill.save()
            messages.success(request,'Final Skill Score is Successfully Update')
            return HttpResponseRedirect(url)
    return render(request,'login_page.html')

@login_required(login_url='/')
def teacher_system(request):
    if request.user.user_type == '4':
        report =  Groups_teachers.objects.filter(
            id_teacher = request.user.teacher.id,
        ).order_by('id').reverse()

        total_class = report.count()

        total_salary = report.aggregate(total=Sum(F('pay__salary')))

        
        paginator = Paginator(report, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        report = paginator.get_page(page_number)

        dic = {
            "report":report,
            'total_class':total_class,
            'total_salary':total_salary['total'],
        }
        return render(request,'teacher_system/home.html',dic)
    return render(request,'login_page.html')

#present
@login_required(login_url='/')
def present(request):
    if request.user.user_type == '4':
        if request.method == "POST":
            total = int(request.POST.get('total'))
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
            messages.success(request,'Do Attendance Successfully')
            return redirect('my-profile')
        else:
            messages.warning(request,'Some Problem try again')
            return redirect('my-profile')
    return render(request,'login_page.html')

@login_required(login_url='/')
def attendance(request,pk):
    if request.user.user_type == '4':
        present = Present.objects.filter(group_student = pk,
            timestamp__year = datetime.now().year, 
            timestamp__month = datetime.now().month,
        )
        dic = {
            'present':present,
        }
        return render(request,'teacher_system/attendance.html',dic)
    return render(request,'login_page.html')