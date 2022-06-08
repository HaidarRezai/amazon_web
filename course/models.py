from django.db import models
from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     usera = (
#         (1,'Admin'),
#         (2,'HOD'),
#         (3,'Staff'),
#         (4,'Teacher'),
#     )
#     user_type = models.CharField(choices=usera,max_length=50,default=1)
#     profile_pic = models.ImageField(upload_to='media/profile_pic')
    
# class Group(models.Model):
#     name_class      = models.CharField(max_length = 50)
#     waqt            = models.DateTimeField()
#     number_class    = models.CharField(max_length = 50)
#     start_date      = models.DateTimeField()
#     end_date        = models.DateTimeField()
#     fees            = models.CharField(max_length = 50)
#     timestamp   = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return str(self.name_class)

# class Teacher(models.Model):
#     admin       = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     name        = models.CharField(max_length = 50)
#     last_name   = models.CharField(max_length = 50)
#     father_name = models.CharField(max_length = 50)
#     phone_one   = models.CharField(max_length = 50)
#     phone_tow   = models.CharField(max_length = 50)
#     # phone_tow   = models.CharField(max_length = 50)
#     photo       = models.ImageField(null= True ,blank=True)
#     degree_edu  = models.CharField(max_length = 50)
#     address_one = models.CharField(max_length = 50)
#     address_tow = models.CharField(max_length = 50)
#     idcord      = models.CharField(max_length = 50)
#     level       = models.CharField(max_length = 50)
#     timestamp   = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return str(self.name)+" "+ str(self.last_name) 
        
# class Teacher_group(models.Model):
#     teacher     = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     group       = models.ForeignKey(Group, on_delete=models.CASCADE)
#     timestamp   = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return str(self.teacher)+" "+ str(self.group) 

# class Salary(models.Model):
#     salary     = models.PositiveIntegerField()
#     baqiyat     = models.IntegerField()
#     pish_pay    = models.PositiveIntegerField()
#     teacher_group = models.ForeignKey(Teacher_group, on_delete=models.CASCADE)
#     timestamp   = models.DateTimeField(auto_now_add=True)
#     def __int__(self):
#         return str(self.slary)

# class Student(models.Model):
#     name        = models.CharField(max_length = 50)
#     last_name   = models.CharField(max_length = 50)
#     father_name = models.CharField(max_length = 50)
#     phone_one   = models.CharField(max_length = 50)
#     phone_tow   = models.CharField(max_length = 50)
#     photo       = models.ImageField(null= True ,blank=True)
#     degree_edu  = models.CharField(max_length = 50)
#     address_one = models.CharField(max_length = 50)
#     address_tow = models.CharField(max_length = 50)
#     idcord      = models.CharField(max_length = 50)
#     level       = models.CharField(max_length = 50)
#     timestamp   = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return str(self.name)+" "+ str(self.last_name) 
 

# class Student_group(models.Model):
#     fee         = models.IntegerField()
#     group       = models.ForeignKey(Group, on_delete=models.CASCADE)
#     student     = models.ForeignKey(Student, on_delete=models.CASCADE)
#     timestamp   = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return str(self.student)+" "+ str(self.group) 
 
# class Payment(models.Model):
#     activate_class = models.IntegerField()
#     home_work      = models.IntegerField()
#     score          = models.IntegerField()
#     full_score     = models.DateTimeField(auto_now_add=True)
#     student_group  = models.ForeignKey(Student_group, on_delete=models.CASCADE)
#     timestamp      = models.DateTimeField(auto_now_add=True)
#     def __int__(self):
#         return str(self.activate_class)  

# class Presend(models.Model):
#     presend        = models.IntegerField()
#     absend         = models.IntegerField()
#     student_group  = models.ForeignKey(Student_group, on_delete=models.CASCADE)
#     timestamp      = models.DateTimeField(auto_now_add=True)
#     def __int__(self):
#         return str(self.presend)