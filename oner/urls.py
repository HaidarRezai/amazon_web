from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from oner import views
urlpatterns = [
    path("oner", views.oner, name="oner"),
    path("staff_add", views.staff_add, name="staff-add"),
    path("staff_all", views.staff_all, name="staff-all"),
    path("staff_save", views.staff_save, name="staff-save"),
    path("report_account", views.acounting, name="report-account"),
    path("staff_profile/<int:pk>/", views.staff_profile, name="staff-profile"),
    path("staff_update/<int:pk>/", views.staff_update, name="staff-update"),
    path("staff-doupdate", views.staff_doupdate, name="staff-doupdate"),
    path("staff-delete/<int:pk>/", views.staff_delete, name="staff-delete"),
    path("staff_dodelete/<int:pk>/", views.staff_dodelete, name="staff-dodelete"),
   
    # path("search_acounting", views.search_acounting, name="search-acounting"),
]