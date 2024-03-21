from django.urls import path
from EmployeeApp import views



urlpatterns = [
    path('EmployeeDashboard/',views.EmployeeDashboard),
    path('EmployeeProject/',views.EmployeeProject),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('leave/', views.leave, name='leave'),
]
