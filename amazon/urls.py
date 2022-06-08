from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from amazon import views, views_student,views_teacher,views_class

urlpatterns = [
    
    # path('index', views.index, name='index'),

    path('', views.LOGIN, name='login'),

    path('dologin', views.dologin, name='dologin'),
    path("doLogout", views.doLogout, name="logout"),

    #profile
    path("profile", views.PROFILE, name="profile"),
    path("profile_update", views.profile_update, name="profile-update"),
    path("doprofile_update", views.doprofile_update, name="doprofile-update"),

    #Teacher
    path("teacher_add", views_teacher.teacher_add, name="teacher-add"),
    path("teacher_save", views_teacher.teacher_save, name="teacher-save"),
    path("teacher_all", views_teacher.teacher_all, name="teacher-all"),
    path("teacher_profile/<int:pk>/", views_teacher.teacher_profile, name="teacher-see"),
    path("teacher_update/<int:pk>/", views_teacher.teacher_update, name="teacher-update"),
    path("teacher_doupdate", views_teacher.teacher_doupdate, name="teacher-doupdate"),
    path("teacher_delete/<int:pk>/", views_teacher.teacher_delete, name="teacher-delete"),
    path("teacher_dodelete/<int:pk>/", views_teacher.teacher_dodelete, name="teacher-dodelete"),
    path("list_payed/<int:pk>/", views_teacher.list_payed, name="list-payed"),
    
    #Salary
    path("pay_salary", views_teacher.pay_salary, name="pay-salary"),
    path("payment", views_teacher.payment, name="payment"),
    path("show_payment/<int:pk>/", views_teacher.show_payment, name="show-payment"),
    # path("pay_salary_tow", views_teacher.pay_salary_tow, name="pay-salary_tow"),
    path("show_salary/<int:pk>/", views_teacher.show_salary, name="show-salary"),
    # path("update_salary", views_teacher.update_salary, name="update-salary"),
    path("more_salary/<int:pk>/<int:id_tea>/", views_teacher.more_salary, name="more-salary"),
    # path("pay_baqi", views_teacher.pay_baqi, name="pay-baqi"),
    path("pay_month", views_teacher.pay_month, name="pay-month"),
    # path("show_remaind_month/<int:pk>/", views_teacher.show_remaind_month, name="show_remaind_month"),
    # path("pay_remaind_month", views_teacher.pay_remaind_month, name="pay-remaind-month"),

    #Class
    path("class_add", views_class.class_add, name="class-add"),
    path("class_delete/<int:pk>/", views_class.class_delete, name="class-delete"),
    path("class_dodelete/<int:pk>/", views_class.doclass_delete, name="class-dodelete"),
    path("class_save", views_class.class_save, name="class-save"),
    path("class_update/<int:pk>/", views_class.class_update, name="class-update"),
    path("class_doupdate", views_class.class_doupdate, name="class-doupdate"),
    path("class_info/<int:pk>/", views_class.class_info, name="class-info"),
    path("class_score/<int:pk>/", views_class.class_score, name="class-score"),
    path("class_report/<int:pk>/", views_class.class_report, name="class-report"),
    path("class_resultcart/<int:pk>/", views_class.class_resultcart, name="class-resultcart"),
    path("attendance_show/<int:pk>/", views_class.attendance_show, name="attendance-show"),
    path("show_all", views_class.show_all, name="show-all"),
    path("finisht", views_class.finisht, name="finisht"),

    #Present
    path("present", views_class.present, name="present"),
    path("attendance/<int:pk>/", views_class.attendance, name="attendance"),

    #acounting
    path("acounting", views_class.acounting, name="acounting"),
    path("input_add", views.input_add, name="input-add"),
    path("output_add", views.output_add, name="output-add"),



    #Students
    path("new_student", views_student.new_student, name="new-student"),
    path("add_student", views_student.add_student, name="add-student"),
    path("all_student", views_student.all_student, name="all-student"),
    path("student_profile/<int:pk>/", views_student.student_profile, name="student-profile"),
    path("student_update/<int:pk>/", views_student.student_update, name="student-update"),
    path("student_doupdate", views_student.student_doupdate, name="student-doupdate"),
    path("student_delete/<int:pk>/", views_student.student_delete, name="student-delete"),
    path("student_dodelete/<int:pk>/", views_student.student_dodelete, name="student-dodelete"),
    path("register_class", views_student.register_class, name="register-class"),
    path("class_info_student/<int:pk>/", views_student.class_info, name="class-info_student"),
    path("deselect_class/<int:pk>/", views_student.deselect_class, name="deselect-class"),
    path("dodeselect_class/<int:pk>/", views_student.dodeselect_class, name="dodeselect-class"),
    path("change_class", views_student.change_class, name="change-class"),
    path("exam", views_student.exam, name="exam"),
    path("add_exam", views_student.add_exam, name="add-exam"),
    
    #Score Set
    path("set_score", views_student.set_score, name="set-score"),
    path("update_score", views_student.update_score, name="update-score"),
    path("middle_skill", views_student.middle_skill, name="middle-skill"),
    path("update_middle_skill", views_student.update_middle_skill, name="update_middle-skill"),
    path("final_skill", views_student.final_skill, name="final-skill"),
    path("update_final_skill", views_student.update_final_skill, name="update_final-skill"),

    path("pay_baqi_student", views_student.pay_baqi_student, name="pay-baqi_student"),
    # acounting students for class
    path("acount_stu", views_student.acount_stu, name="acount-stu"),
    path("charge_stu", views_student.charge_stu, name="charge-stu"),

    #Qars
    path("remainder", views.qars, name="qars"),
    path("about_us", views.about_us, name="about_us"),
    
    # path("teacher", views_teacher.teacher, name="teacher"),
    
    #profile Update
    # path("teacher_update", views.teacher_update, name="teacher-update"),
    

    path('home', views_teacher.home, name='home'),

]