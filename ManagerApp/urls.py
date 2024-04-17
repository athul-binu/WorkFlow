from django.contrib import admin
from django.urls import path,include
from ManagerApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('accounts/', include('django.contrib.auth.urls'))
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
    path('leaverequest/', views.manager_leave, name='leaverequest'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('RecruitRequest/', views.RecruitRequest, name='RecruitRequest'),
    path('job/', views.job_application_view, name='job'),
    path('addtask/<int:task_id>', views.edit_task, name='addtask'),
    
]



