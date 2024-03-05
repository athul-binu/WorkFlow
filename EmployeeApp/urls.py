from django.contrib import admin
from django.urls import path
from EmployeeApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('project/', views.create_project, name='project_overview'),
    path('ManagerDashboard/', views.ManagerDashboard, name='ManagerDashboard'),
]
