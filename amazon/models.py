from turtle import position
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    usera = (
        (1,'Admin'),
        (2,'HOD'),
        (4,'Teacher'),
    )
    user_type = models.CharField(choices=usera,max_length=50,default=2)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

    def __str__(self):
        return str(self.id)

class Teacher(models.Model):
    admin       = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    father_name = models.CharField(max_length = 50)
    phone_one   = models.CharField(max_length = 50)
    phone_tow   = models.CharField(max_length = 50)
    degree_edu  = models.CharField(max_length = 50)
    address_one = models.CharField(max_length = 50)
    address_tow = models.CharField(max_length = 50)
    idcord      = models.CharField(max_length = 50)
    level       = models.CharField(max_length = 50)
    active        = models.CharField(max_length = 3, default = 1)
    amount_salary = models.IntegerField(default =0)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Staff(models.Model):
    admin       = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    father_name = models.CharField(max_length = 50)
    phone_one   = models.CharField(max_length = 50)
    phone_tow   = models.CharField(max_length = 50)
    degree_edu  = models.CharField(max_length = 50)
    address_one = models.CharField(max_length = 50)
    address_tow = models.CharField(max_length = 50)
    idcord      = models.CharField(max_length = 50)
    amount_salary = models.IntegerField(default =0)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Group(models.Model):
    subject       = models.CharField(max_length = 50)
    start_time    = models.TimeField()
    number_class  = models.CharField(max_length = 50)
    start_date    = models.DateTimeField()
    end_date      = models.DateTimeField()
    fees          = models.IntegerField()
    active        = models.CharField(max_length = 8, default = 1)
    timestamp     = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Input(models.Model):
    datils        = models.CharField(max_length = 150)
    money         = models.IntegerField()
    by            = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp     = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return int(self.id)

class Output(models.Model):
    datils        = models.TextField()
    money         = models.IntegerField()
    by            = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp     = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return int(self.id)

class Groups_teachers(models.Model):
    id_teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='teacher_one')
    id_group = models.ForeignKey(Group,on_delete=models.CASCADE)
    position_teacher = models.CharField(max_length = 5,default="one")
    include = models.CharField(max_length = 5,default="one")
    timestamp     = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return int(self.id)

class Pay(models.Model):
    group_teacher = models.OneToOneField(Groups_teachers,on_delete=models.CASCADE)
    salary      = models.PositiveIntegerField()
    # baqiyat     = models.IntegerField()
    active      = models.CharField(max_length = 3, default = 1)
    by          = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return str(self.slary)

class Pay_month(models.Model):
    teacher     = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    salary      = models.PositiveIntegerField()
    baqiyat     = models.IntegerField()
    by          = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return str(self.slary)

class Amount_salary(models.Model):
    group_teacher = models.OneToOneField(Groups_teachers,on_delete=models.CASCADE)
    type_salary   = models.CharField(max_length = 50)
    salary        = models.PositiveIntegerField()
   
#start
class Total_salary(models.Model):
    teacher     = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    amount      = models.IntegerField()
    by          = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp   = models.DateTimeField(auto_now_add=True)
#end

#start
class Payment(models.Model):
    teacher     = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    amount      = models.IntegerField()
    by          = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp   = models.DateTimeField(auto_now_add=True)
#end


#student
class Student(models.Model):
    student_pic = models.ImageField(upload_to='media/student_pic')
    first_name  = models.CharField(max_length = 50)
    last_name   = models.CharField(max_length = 50)
    father_name = models.CharField(max_length = 50)
    idcard      = models.CharField(max_length = 50)
    job         = models.CharField(max_length=50)
    phone_one   = models.CharField(max_length = 50)
    phone_tow   = models.CharField(max_length = 50)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)


class Acount_stu(models.Model):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    amount  = models.IntegerField(default=0)
    datils  = models.TextField()
    by      = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)

class Exam(models.Model):
    first_name  = models.CharField(max_length = 50)
    last_name   = models.CharField(max_length = 50)
    father_name = models.CharField(max_length = 50)
    fees        = models.PositiveIntegerField()
    level       = models.CharField(max_length = 50)
    phone_one   = models.CharField(max_length = 50)
    phone_tow   = models.CharField(max_length = 50)
    by          = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Address_student(models.Model):
    student     = models.OneToOneField(Student,on_delete=models.CASCADE)
    province_one = models.CharField(max_length = 150)
    village_one  = models.CharField(max_length = 150)
    province_tow = models.CharField(max_length = 150)
    village_tow  = models.CharField(max_length = 150)
    new_address  = models.TextField()
    def __str__(self):
        return str(self.id)

class Education_student(models.Model):
    education = (
        (1,'student_school'),
        (2,'graduate_school'),
        (3,'student_university'),
        (4,'graduate_university'),
    )
    student = models.OneToOneField(Student,on_delete = models.CASCADE)
    level   = models.CharField(choices = education,max_length = 150)
    form    = models.CharField(max_length = 150)
    def __str__(self):
        return str(self.id)

class Groups_students(models.Model):
    id_student = models.ForeignKey(Student,on_delete=models.CASCADE)
    id_group = models.ForeignKey(Group,on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return int(self.id)

class Score(models.Model):
    group_student = models.OneToOneField(Groups_students,on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    final_score = models.PositiveIntegerField()
    activate = models.PositiveIntegerField()
    home_work = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

class Middle_skill(models.Model):
    group_student = models.OneToOneField(Groups_students,on_delete=models.CASCADE)
    reading = models.PositiveIntegerField(default=0)
    writing = models.PositiveIntegerField(default=0)
    listening = models.PositiveIntegerField(default=0)
    speaking = models.PositiveIntegerField(default=0)
    
    def __int__(self):
        return int(self.id)
    
class Final_skill(models.Model):
    group_student = models.OneToOneField(Groups_students,on_delete=models.CASCADE)  
    reading = models.PositiveIntegerField(default=0)
    writing = models.PositiveIntegerField(default=0)
    listening = models.PositiveIntegerField(default=0)
    speaking = models.PositiveIntegerField(default=0)

    def __int__(self):
        return int(self.id)

class Fees(models.Model):
    group_student  = models.OneToOneField(Groups_students,on_delete=models.CASCADE)
    fees = models.PositiveIntegerField()
    descount = models.PositiveIntegerField()
    baqi = models.PositiveIntegerField()
    by  = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    timestamp   = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return int(self.id)

class Present(models.Model):
    group_student   = models.ForeignKey(Groups_students,on_delete=models.CASCADE)
    present         = models.PositiveIntegerField()
    timestamp       = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
