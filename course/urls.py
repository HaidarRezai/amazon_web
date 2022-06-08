from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from course import views, views_teacher

urlpatterns = [
    
    path('index', views.index, name='index'),
    path('', views.LOGIN, name='login'),
    path('dologin', views.dologin, name='dologin'),
    path("doLogout", views.doLogout, name="logout"),

    #profile
    path("profile", views.PROFILE, name="profile"),


    path("teacher", views_teacher.teacher, name="teacher"),
    
    #profile Update
    path("teacher_update", views.teacher_update, name="teacher-update"),
    

    path('home', views_teacher.home, name='home'),

]