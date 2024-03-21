from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
# from .forms import ProjectForm, TaskForm, TeamForm, TeamMembersForm
from ManagerApp.models import Manager, Project, Task, Team, TeamMembers
from EmployeeApp.models import Employee,Event,ScheduledEvent,Attendance
from django.urls import reverse
from django.forms import modelformset_factory
from django.utils import timezone
from .form import AttendanceForm

def EmployeeDashboard(request):
    username = request.session.get('username')
    
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    employee = Employee.objects.get(Username=username)
    team_members = TeamMembers.objects.filter(TeamID__in=TeamMembers.objects.filter(EmployeeID=employee.EmployeeID).values_list('TeamID', flat=True)).exclude(EmployeeID=employee.EmployeeID)
    
    events = Event.objects.filter(EmployeeID=employee)
    scheduled_events = ScheduledEvent.objects.filter(EmployeeID=employee)
    
    high_priority_events = events.filter(EventPriority="High")
    low_priority_events = events.filter(EventPriority="Low")
    
    context = {
        'employee': employee,
        'teammembers': team_members,
        'high_priority_events': high_priority_events,
        'low_priority_events': low_priority_events,
        'scheduled_events': scheduled_events
    }
    return render(request, 'Employee/employee_dashboard.html', context)


def EmployeeProject(request):
    username = request.session.get('username')
    
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    employee = Employee.objects.get(Username=username)
    team_members = TeamMembers.objects.filter(TeamID__in=TeamMembers.objects.filter(EmployeeID=employee.EmployeeID).values_list('TeamID', flat=True)).exclude(EmployeeID=employee.EmployeeID)
    team_memberdata = TeamMembers.objects.filter(EmployeeID=employee)
    team_tasks =[]
    for team_member in team_members:
        # team = team_member.TeamID
        team = Team.objects.filter(TeamID=team_member.TeamID_id)   
        print(team)
        team_tasks.extend(team)

    # projects = Project.objects.filter(EmployeeID=employee)
    
    context = {
        'employee': employee,
        'teammembers': team_members,
        # 'projects': projects,
        'team':team_tasks
        
    }
    
    return render(request, 'Employee/employee_project.html', context)



def mark_attendance(request):
    username = request.session.get('username')
    
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    employee = Employee.objects.get(Username=username)
    current_date = timezone.now().date()
    
    try:
        attendance = Attendance.objects.get(EmployeeID=employee, Date=current_date)
        status = attendance.Status
        message = "Attendance for today is already marked."
    except Attendance.DoesNotExist:
        attendance = None
        status = "Offline"

    if request.method == 'POST':
        if attendance:
            messages.error(request, 'Attendance for today is already marked.')
            return redirect('/mark_attendance')
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.EmployeeID = employee
            attendance.Date = current_date
            attendance.Status = "Active"
            attendance.save()
            return redirect('/mark_attendance')
    else:
        form = AttendanceForm(initial={'EmployeeID': employee.EmployeeID, 'Status': 'Active'})
    return render(request, 'Employee/employee_attendance.html', {'form': form, 'employee_id': employee.EmployeeID, 'status': status,'employee': employee})
