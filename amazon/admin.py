from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserModel(UserAdmin):
    list_display =['username','user_type']


admin.site.register(CustomUser,UserModel)
admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Staff)
admin.site.register(Groups_teachers)
admin.site.register(Pay_month)
# ///////
admin.site.register(Total_salary)
admin.site.register(Acount_stu)
admin.site.register(Payment)
# ////////

admin.site.register(Pay)
admin.site.register(Input)
admin.site.register(Output)
admin.site.register(Exam)
admin.site.register(Amount_salary)
admin.site.register(Student)
admin.site.register(Address_student)
admin.site.register(Education_student)
admin.site.register(Groups_students)
admin.site.register(Score)
admin.site.register(Fees)
admin.site.register(Present)
admin.site.register(Middle_skill)
admin.site.register(Final_skill)