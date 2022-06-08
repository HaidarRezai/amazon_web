from ast import And
from datetime import datetime
from functools import cache
from math import remainder
import math
from typing import ChainMap
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from amazon.models import *
from django.db.models import F, Sum, Avg,Count
from django.contrib import messages
from amazon.views import profile_update
from django.core.paginator import Paginator
from django.db.models import Q

@login_required(login_url='/')
def new_student(request):
    return render(request, 'student/new_student.html')

@login_required(login_url='/')
def add_student(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            father_name = request.POST.get('father_name')
            # idcard = request.POST.get('idcard')
            # job = request.POST.get('job')
            # phone_one = request.POST.get('phone_one')
            # phone_tow = request.POST.get('phone_tow')
            # province_one = request.POST.get('province_one')
            # village_one = request.POST.get('village_one')
            # province_tow = request.POST.get('province_tow')
            # village_tow = request.POST.get('village_tow')
            # new_address = request.POST.get('new_address')
            # level = request.POST.get('level')
            # form = request.POST.get('form')
            # student_pic = request.FILES.get('student_pic')

            student = Student(
                student_pic= '',
                first_name = first_name,
                last_name = last_name,
                father_name = father_name,
                idcard = '',
                job = '',
                phone_one = '',
                phone_tow = '',
            )
            student.save()

            address_student = Address_student(
                student = student,
                province_one = '',
                village_one = '',
                province_tow = '',
                village_tow = '',
                new_address = 'Address: ',
            )
            address_student.save()

            education_student = Education_student(
                student = student,
                level = '',
                form = '',
            )
            education_student.save()

            acount_stu = Acount_stu(
                student = student,
                amount = 0,
                datils = '',
                by = CustomUser.objects.get(id = request.user.id),
            )
            acount_stu.save()

            messages.success(request,student.first_name + " " + student.last_name + ' Student Successfully Save')
            return redirect('all-student')
        
        return render(request, 'student/new_student.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def exam(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            search = request.POST['search']
            multi = Q(Q(first_name__icontains=search)|Q(phone_one__icontains=search))
            exam = Exam.objects.filter(multi)
            dic = {
            'exam':exam,
            }
        else:
            exam = Exam.objects.all().order_by('id').reverse()
            paginator = Paginator(exam, 8) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            exam = paginator.get_page(page_number)
            dic = {
            'exam':exam,
            }
        return render(request,'student/exam.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def add_exam(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            father_name = request.POST.get('father_name')
            fees = int(request.POST.get('fees'))
            phone_one = request.POST.get('phone_one')
            phone_tow = request.POST.get('phone_tow')
            level = request.POST.get('level')
            if father_name == "":
                father_name = ''
            elif last_name == "":
                last_name = ''
            elif phone_tow == '':
                phone_tow = ''
            elif level == '':
                level = ''
            try:
                exam = Exam(
                first_name = first_name,
                last_name = last_name,
                father_name = father_name,
                fees = fees,
                phone_one = phone_one,
                phone_tow = phone_tow,
                level = level,
                by = CustomUser.objects.get(id = request.user.id)
                )
                exam.save()
                input = Input(
                    datils = "In Exam Student",
                    money = fees,
                    by = CustomUser.objects.get(id = request.user.id)
                )
                input.save()
                messages.success(request,exam.first_name + " " + exam.last_name + ' Student Successfully Save')
                return redirect('exam')
            except:
                messages.warning(request,exam.first_name + " " + exam.last_name + ' Student Faild Save')
                return redirect('exam')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def all_student(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            search = request.POST['search']
            multi = Q(Q(first_name__icontains=search)|Q(id__icontains=search)|Q(phone_one__icontains=search))
            student = Student.objects.filter(multi)
            dic={
                'student':student,
                }
        # elif request.method == "GET":
        #     search = request.POST['search']
        #     student = Student.objects.filter(id__contains = search)
        #     dic={
        #         'student':student,
        #         }
        else:
            student = Student.objects.all().order_by('id').reverse()
            
            paginator = Paginator(student, 8) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            student = paginator.get_page(page_number)

            dic={
                'student':student,
            }
        return render(request,'student/all_students.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def student_profile(request,pk):
    if request.user.user_type == '1':
        student = Student.objects.get(id = pk)
        
        group = Groups_students.objects.filter(
            id_student = pk,
            ).order_by('id').reverse()
        
        group_all = Group.objects.filter(
            active = 1,
        ).order_by('id').reverse()

        remainder = group.aggregate(total=Sum(F('fees__baqi')))
        to_fees = group.aggregate(total=Sum(F('fees__fees')))
        
        paginator = Paginator(group, 6) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        group = paginator.get_page(page_number)

        dic={
            "student":student,
            "group":group,
            "group_all":group_all,
            'remainder':remainder['total'],
            'to_fees':to_fees['total'],
        }
        return render(request,'student/student_profile.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def student_update(request,pk):
    if request.user.user_type == '1':
        student = Student.objects.get(id=pk)
        
        dic={
            "student":student,
        }
        return render(request,'student/update_student.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def student_doupdate(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            father_name = request.POST.get('father_name')
            idcard = request.POST.get('idcard')
            job = request.POST.get('job')
            phone_one = request.POST.get('phone_one')
            phone_tow = request.POST.get('phone_tow')
            province_one = request.POST.get('province_one')
            village_one = request.POST.get('village_one')
            province_tow = request.POST.get('province_tow')
            village_tow = request.POST.get('village_tow')
            new_address = request.POST.get('new_address')
            level = request.POST.get('level')
            form = request.POST.get('form')
            student_id = request.POST.get('student_id')
            student_pic = request.FILES.get('student_pic')
        

            student = Student.objects.get(id = student_id)
            if student_pic !=None and student_pic != "":
                student.student_pic = student_pic
            student.first_name = first_name
            student.last_name = last_name
            student.father_name = father_name
            student.idcard = idcard
            student.job = job
            student.phone_one = phone_one
            student.phone_tow = phone_tow

            student.save()

            address_student = Address_student.objects.get(student__id = student_id)
            address_student.student = student
            address_student.province_one = province_one
            address_student.village_one = village_one
            address_student.province_tow = province_tow
            address_student.village_tow = village_tow
            address_student.new_address = new_address

            address_student.save()

            education_student = Education_student.objects.get(student__id = student_id)
            education_student.student = student
            if level !=None and level != "":
                education_student.level = level
            education_student.form = form
            
            education_student.save()
            
            url = "student_profile/{}/".format(student_id)
            messages.success(request,'Record Are Successfully upated')
            return HttpResponseRedirect(url)
            
        return render(request,'teacher/update_teacher.html')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def student_delete(request,pk):
    if request.user.user_type == '1':
        student = Student.objects.get(id = pk)
        dic={
            "student":student,
        }
        return render(request,'student/delete.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def student_dodelete(request,pk):
    if request.user.user_type == '1':
        student = Student.objects.get(id = pk)

        student.delete()
        messages.success(request,'Record Are Successfully Delete')
        return redirect('all-student')
    else:
        return render(request,'login_page.html')

#select class
@login_required(login_url='/')
def register_class(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            id_group = request.POST.get('id_group')
            id_student = request.POST.get('id_student')
            fees = int(request.POST.get('fees'))
            choose = request.POST.get('choose')
            # descount = int(request.POST.get('descount'))
            # baqi = int(request.POST.get('baqi'))
            des = 0
            baqi = 0
            url = 'student_profile/{}/'.format(id_student)
            if id_group == "null":
                messages.warning(request,' On Register Select class')
                return redirect('all-student')
            else:
                group = Group.objects.get(id = id_group)
                if fees < group.fees:
                    if choose == 'dec':
                        des = 100-((fees*100)/group.fees)
                    else: 
                        baqi = group.fees - fees
                elif fees == group.fees:
                    des = 0
                    baqi = 0
                else:
                    messages.warning(request,'Fee is alat of range')
                    return HttpResponseRedirect(url)
                # total = (descount*fees)/100
                # fees -= total
                # fees -= baqi
                    
                student = Student.objects.get(id = id_student)
                # group = Group.objects.get(id = id_group)
                by = CustomUser.objects.get(id = request.user.id)

                dic={
                    "fees":fees,
                    "baqi":baqi,
                    "descount":math.floor(des),
                    "student":student,
                    "group":group,
                    "by_name":by.first_name,
                    "by_last_name":by.last_name,
                }

                groups_students = Groups_students(
                    id_student = student,
                    id_group = group,
                )
                groups_students.save()
                feesd = Fees(
                    group_student = groups_students,
                    fees = fees,
                    descount = des,
                    baqi = baqi,
                    by = by,
                )
                feesd.save()
                input = Input(
                    datils = 'Registertions Students Class',
                    money = fees,
                    by = CustomUser.objects.get(id = request.user.id)
                )
                input.save()
                messages.success(request,'Class is Successfully Register')
                return render(request,'student/bel.html',dic)
                
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def class_info(request,pk):
    if request.user.user_type == '1':    
        group_student = Groups_students.objects.get(
            id = pk,
        )
        teachers = Groups_teachers.objects.filter(id_group = group_student.id_group.id )
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
            'teachers':teachers,
            'activate':activate,
        }
        return render(request,'student/class_info.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def deselect_class(request,pk):
    if request.user.user_type == '1':
        deselect = Groups_students.objects.get(id = pk)
        dic={
            "deselect":deselect,
        }
        return render(request,'student/deselect_class.html',dic)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def dodeselect_class(request,pk):
    if request.user.user_type == '1':
        deselect = Groups_students.objects.get(id = pk)
        deselect.delete()
        messages.success(request,'Class is Successfully Deselect')
        return redirect('all-student')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def change_class(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            id = request.POST.get('id')

            id_group = request.POST.get('id_group')
            
            url = "class_info_student/{}/".format(id)
            
            id_group = Group.objects.get(id = id_group)

            change = Groups_students.objects.get(id = id)

            fee = Fees.objects.get(group_student = change)

            if fee.descount:
                new_fee = (id_group.fees * fee.descount)/100
            else:
                new_fee = id_group.fees
            result = change.fees.fees-new_fee
            
            if result > 0:
                try:
                    acount_stuo = Acount_stu.objects.get(student = change.id_student)
                    acount_stuo.amount += result
                    acount_stuo.save()
                except:
                    acount_stu = Acount_stu(
                        student = change.id_student,
                        amount = result,
                        datils = 'Change class',
                        by = CustomUser.objects.get(id = request.user.id),
                    )
                    acount_stu.save()

                fee.fees -= result
                change.id_group = id_group
                change.save()
                fee.save()
                
            else:
                if fee.baqi:
                    fee.baqi = (-result)
                else:
                    input = Input(
                    datils = 'Change {} to {}'.format(change.id_group.subject,id_group.subject),
                    money = -result,
                    by = CustomUser.objects.get(id = request.user.id),
                    )
                    input.save()
                fee.fees -= result
                fee.save()

                change.id_group = id_group
                change.save()
            try:
                messages.success(request,'Class is Successfully Changed')
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Class is not Change')
                return redirect('all-student')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def acount_stu(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            try:
                amount = int(request.POST.get('amount'))
                id_student = request.POST.get('id_student')
                acount_stu = Acount_stu.objects.get(student = id_student)
                acount_stu.amount -= amount
                acount_stu.save()
                
                output = Output(
                    datils = 'for account student last',
                    money = amount,
                    by = CustomUser.objects.get(id = request.user.id),
                )
                output.save()
                messages.success(request,'Mony is Successfully take')
                url = "student_profile/{}/".format(id_student)
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Some problem try agin')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def charge_stu(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            try:
                amount = int(request.POST.get('amount'))
                id_student = request.POST.get('id_student')
                acount_stu = Acount_stu.objects.get(student = id_student)
                acount_stu.amount += amount
                acount_stu.save()
                
                input = Input(
                    datils = 'for account student charge',
                    money = amount,
                    by = CustomUser.objects.get(id = request.user.id),
                )
                input.save()
                messages.success(request,'Mony is Successfully charge')
                url = "student_profile/{}/".format(id_student)
                return HttpResponseRedirect(url)
            except:
                messages.warning(request,'Some problem try agin')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def set_score(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        if request.method == "POST":
            set = request.POST.get('set')
            page = request.POST.get('page')
            group_student = request.POST.get('group_student')
            score = request.POST.get('score')
            final_score = request.POST.get('final_score')
            activate = request.POST.get('activate')
            home_work = request.POST.get('home_work')

            url = "class_info_student/{}/".format(group_student)
            
            group_student = Groups_students.objects.get(id = group_student)
            
            score = Score(
                    group_student = group_student,
                    score = score,
                    final_score = final_score,
                    activate = activate,
                    home_work = home_work,
            )
            score.save()
            messages.success(request,'Score is Successfully Set')
            if set == None:
                return HttpResponseRedirect(url)
            else:
                urls = "class_score/{}/?page={}".format(group_student.id_group.id,page)
                return HttpResponseRedirect(urls)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def update_score(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        if request.method == "POST":
            set = request.POST.get('set')
            page = request.POST.get('page')
            group_student = request.POST.get('group_student')
            score = request.POST.get('score')
            final_score = request.POST.get('final_score')
            activate = request.POST.get('activate')
            home_work = request.POST.get('home_work')
            url = "class_info_student/{}/".format(group_student)

            score_update = Score.objects.get(group_student = group_student)
            score_update.score = score
            score_update.final_score = final_score
            score_update.activate = activate
            score_update.home_work = home_work
            score_update.save()
            messages.success(request,'Score is Successfully Update')
            if set == None:
                return HttpResponseRedirect(url)
            else:
                urls = "class_score/{}/?page={}".format(score_update.group_student.id_group.id,page)
                return HttpResponseRedirect(urls)
            
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def pay_baqi_student(request):
    if request.user.user_type == '1':
        if request.method == "POST":
            group_student = request.POST.get('group_student')
            baqi = int(request.POST.get('baqi'))
            url = "class_info_student/{}/".format(group_student)
            by = CustomUser.objects.get(id = request.user.id)

            baqi_pay = Fees.objects.get(group_student = group_student)
            baqi_pay.fees += baqi
            baqi_pay.baqi = 0
            baqi_pay.by = by
            baqi_pay.save()
            input = Input(
                datils = 'Remainder Payed Fees',
                money = baqi,
                by = by,
            )
            input.save()

            messages.success(request,'Remainder is Successfully Payed')
            return HttpResponseRedirect(url)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def middle_skill(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        if request.method == "POST":
            set = request.POST.get('set')
            page = request.POST.get('page')
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "class_info_student/{}/".format(group_student)

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
                if set == None:
                    return HttpResponseRedirect(url)
                else:
                    urls = "class_score/{}/?page={}".format(group_student.id_group.id,page)
                    return HttpResponseRedirect(urls)
            except:
                messages.warning(request,'Middle Skill score is was Set')
                return redirect('all-student')
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def update_middle_skill(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        if request.method == "POST":
            set = request.POST.get('set')
            page = request.POST.get('page')
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "class_info_student/{}/".format(group_student)

            middle_skill = Middle_skill.objects.get(group_student = group_student)

            middle_skill.reading = reading
            middle_skill.writing = writing
            middle_skill.listening = listening
            middle_skill.speaking = speaking
            middle_skill.save()
            messages.success(request,'Middle Skill Score is Successfully Update')
            if set == None:
                return HttpResponseRedirect(url)
            else:
                urls = "class_score/{}/?page={}".format(middle_skill.group_student.id_group.id,page)
                return HttpResponseRedirect(urls)
    else:
        return render(request,'login_page.html')

@login_required(login_url='/')
def final_skill(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        if request.method == "POST":
            set = request.POST.get('set')
            page = request.POST.get('page')
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "class_info_student/{}/".format(group_student)

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
                if set == None:
                    return HttpResponseRedirect(url)
                else:
                    urls = "class_score/{}/?page={}".format(group_student.id_group.id,page)
                    return HttpResponseRedirect(urls)
            except:
                messages.warning(request,'Fanal Skill score is was Set')
                return HttpResponseRedirect(url)
    else:
        return render(request,'login_page.html')

            
@login_required(login_url='/')
def update_final_skill(request):
    if request.user.user_type == '1' or request.user.user_type == '4':
        if request.method == "POST":
            set = request.POST.get('set')
            page = request.POST.get('page')
            group_student = request.POST.get('group_student')
            reading = request.POST.get('reading')
            writing = request.POST.get('writing')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            url = "class_info_student/{}/".format(group_student)

            final_skill = Final_skill.objects.get(group_student = group_student)

            final_skill.reading = reading
            final_skill.writing = writing
            final_skill.listening = listening
            final_skill.speaking = speaking
            final_skill.save()
            messages.success(request,'Final Skill Score is Successfully Update')
            if set == None:
                return HttpResponseRedirect(url)
            else:
                urls = "class_score/{}/?page={}".format(final_skill.group_student.id_group.id,page)
                return HttpResponseRedirect(urls)
    else:
        return render(request,'login_page.html')
