from django.contrib import admin
from django.urls import path
from EmployeeApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('project/<int:project_id>/', views.project_overview, name='project_overview'),
    path('ManagerDashboard/', views.ManagerDashboard, name='ManagerDashboard'),
    path('ManagerProject/', views.ManagerProject, name='ManagerProject'),
    path('ManagerTeam/', views.ManagerTeam, name='ManagerTeam'),
    path('ManagerTask/', views.ManagerTask, name='ManagerTask'),
    path('ManagerProjectAdd/', views.CreateProject, name='ManagerProjectAdd'),
    path('ManagerProjectTask/', views.CreateTask, name='ManagerProjectTask'),
    path('ManagerProjectTeam/', views.CreateTeam, name='ManagerProjectTeam'),
    path('ManagerProjectEdit/<int:project_id>', views.edit_project, name='ManagerProjectEdit'),
     path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),

]
