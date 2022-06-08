from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from teacher import views
urlpatterns = [
    path("teacher_system", views.teacher_system, name="teacher-system"),
    path("my_profile", views.my_profile, name="my-profile"),
    path("teacher_update", views.teacher_update, name="teacher-update"),
    path("my_class/<int:pk>/", views.my_class, name="my-class"),
    path("my_student/<int:pk>/", views.my_student, name="my-student"),

    #Score Set
    path("set_score_student", views.set_score_student, name="set-score-student"),
    path("update_score_student", views.update_score_student, name="update-score-student"),
    path("middle_skill_student", views.middle_skill_student, name="middle-skill-student"),
    path("upd_mid_ski_student", views.upd_mid_ski_student, name="upd-mid-ski-student"),
    path("final_skill_student", views.final_skill_student, name="final-skill-student"),
    path("upd_fin_ski_student", views.upd_fin_ski_student, name="upd-fin-ski-student"),

    #Present
    path("attendance_system", views.present, name="attendance-system"),
    path("doattendance_system/<int:pk>/", views.attendance, name="doattendance-system"),
]   