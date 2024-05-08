from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .forms import ProjectForm, TaskForm, TeamForm, TeamMembersForm,RecruitmentRequestForm
from ManagerApp.models import Manager, Project, Task, Team, TeamMembers
from EmployeeApp.models import Employee,Leave
from django.urls import reverse
from django.forms import modelformset_factory
from EmployeeApp.form import LeaveForm
from django.contrib.auth.decorators import login_required
from HrApp.models import JobApplication,HR,RecruitmentApplication

from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        try:
            manager = Manager.objects.get(Username=username)
        except Manager.DoesNotExist:
            manager = None

        try:
            employee = Employee.objects.get(Username=username)
        except Employee.DoesNotExist:
            employee = None
            
        try:
            hr = HR.objects.get(Username=username)
        except HR.DoesNotExist:
            hr = None


        if not manager and not employee and not hr:
            messages.error(request, 'Username does not exist. Please try again.')
            return redirect("/")

        if role == 'admin' and manager:
            if password == manager.Password:
                # Set session data
                request.session['username'] = username
                request.session['role'] = role
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        elif role == 'manager' and manager:
            if password == manager.Password:
                # Set session data
                request.session['username'] = username
                request.session['role'] = role
                return redirect('/ManagerDashboard')  # Adjust the URL name as per your project
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        elif role == 'employee' and employee:
            if password == employee.Password:
                # Set session data
                request.session['username'] = username
                request.session['role'] = role
                return redirect('/EmployeeDashboard')  # Adjust the URL name as per your project
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        elif role == 'hr' and hr:
            if password == hr.Password:
            # Assuming you have an 'hr_dashboard' named URL pattern
                request.session['username'] = username
                request.session['role'] = role
                return redirect('/HrDashboard')  # Adjust the URL name as per your project
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return HttpResponse("Invalid role")
    return render(request, 'login.html')


def logout_view(request):
    # Clear session data
    logout(request)
    request.session.clear()
    return redirect('login')

def ManagerDashboard(request):
    # Retrieve the username from the session
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    # Query projects associated with the manager
    projects = Project.objects.filter(ManagerID=manager)
    employees = Employee.objects.all()
    employeesCount = employees.count()
    leave=Leave.objects.all()
    leaveCount = leave.count()
    project_count = projects.count()
    # Initialize empty lists to store task and team data
    task_data = []
    team_data = []
    
    # Iterate through each project to retrieve associated tasks and teams
    for project in projects:
        tasks = Task.objects.filter(ProjectID=project.ProjectID)
        for task in tasks:
            # Retrieve teams associated with the current task
            teams = Team.objects.filter(TaskID=task.TaskID)

            # Extend the team_data list with teams
            team_data.extend(teams)
        # Extend the task_data list with tasks
        task_data.extend(tasks)

    
    # Prepare the context to pass to the template
    context = {
        'manager': manager,
        'projects': projects,
        'task_data': task_data,
        'team_data': team_data,
        'project_count': project_count,
        'employeesCount':employeesCount,
        'leave':leaveCount
    }
    


    return render(request, "Manager/manager_dashboard.html", context)


def ManagerProject(request):
    # Retrieve the username from the session
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    # Query projects associated with the manager
    projects = Project.objects.filter(ManagerID=manager)
    
    # Initialize empty lists to store task and team data
    task_data = []
    team_data = []
    
    # Iterate through each project to retrieve associated tasks and teams
    for project in projects:
        tasks = Task.objects.filter(ProjectID=project.ProjectID)
        for task in tasks:
            # Retrieve teams associated with the current task
            teams = Team.objects.filter(TaskID=task.TaskID)
            # Extend the team_data list with teams
            team_data.extend(teams)
        # Extend the task_data list with tasks
        task_data.extend(tasks)
        
    context = {
        'manager': manager,
        'projects': projects,
        'task_data': task_data,
        'team_data': team_data,
    }
    
    if request.method == "POST":
        searchdata = request.POST.get("search")
        projects = Project.objects.filter(Q(ProjectID__icontains=searchdata) | Q(task__Title__icontains=searchdata) | Q(task__team__TeamName__icontains=searchdata) | Q(task__team__TeamLead__FirstName__icontains=searchdata) | Q(task__team__TeamLead__LastName__icontains=searchdata))
        
        # Clear task_data and team_data before populating them with search results
        task_data.clear()
        team_data.clear()
        
        for project in projects:
            tasks = Task.objects.filter(ProjectID=project.ProjectID)
            for task in tasks:
                teams = Team.objects.filter(TaskID=task.TaskID)
                team_data.extend(teams)
            task_data.extend(tasks)
            
        context = {
            'manager': manager,
            'projects': projects,
            'task_data': task_data,
            'team_data': team_data,
        }
        
    return render(request, "Manager/manager_projectoverview.html", context)



def ManagerTeam(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    # Query projects associated with the manager
    team_members = []  # Initialize empty list to store team members
    
    projects = Project.objects.filter(ManagerID=manager)
    for project in projects:
        # Query team members associated with the current project
        project_team_members = TeamMembers.objects.filter(TeamID__TaskID__ProjectID=project)
        # Extend the list of team members with those from the current project
        team_members.extend(project_team_members)
    

    

    if request.method == 'POST':
        searchdata = request.POST.get("search")
        team_members.clear()
        project_team_members = TeamMembers.objects.filter(Q(EmployeeID__FirstName__icontains=searchdata)|Q(TeamID__TeamName__icontains=searchdata)|Q(EmployeeID__Email__icontains=searchdata))
        # Extend the list of team members with those from the current project
        team_members.extend(project_team_members)
    context = {
        'manager': manager,
        'projects': projects,
        'users': team_members,  # Pass the list of team members to the template
    }
        
    return render(request, "Manager/manager_team.html", context)






def ManagerTask(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    projects = Project.objects.filter(ManagerID=manager)
    managertaskdata=[]
    for project in projects:
        manager_tasks = Task.objects.filter(ProjectID=project)
        managertaskdata.extend(manager_tasks)

    
    content ={
        "manager_tasks": managertaskdata,
        'manager': manager,
    }
    return render(request,"Manager/manager_Task.html",content)




def project_overview(request, project_id):
    
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    # Retrieve project details
    project = Project.objects.get(ProjectID=project_id)

    # Retrieve tasks related to the project
    tasks = Task.objects.filter(ProjectID=project_id)
    datateam=[]
    # Retrieve team related to the project
        # team = Team.objects.filter(TaskID=task.TaskID)
    team = Team.objects.filter(TaskID__ProjectID=project_id)
    
    for team in team:
        team_members = TeamMembers.objects.filter(TeamID=team.TeamID)
            

    # Retrieve team members related to the team
    

    context = {
        'manager': manager,
        'project': project,
        'tasks': tasks,
        'team': team,
        'team_members': team_members
    }

    return render(request, 'Manager/manager_project.html', context)
def CreateProject(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    if request.method == 'POST':
        
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.ManagerID = manager
            project.save()

            return redirect('/ManagerProject')
    else:
        project_form = ProjectForm()
    context ={
        'manager': manager,
        'project_form': project_form,
        
        
        }
    
    return render(request, 'Manager/manager_projectadd.html', context)


    
def CreateTask(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    project=Project.objects.filter(ManagerID=manager)
    if request.method == 'POST':
        
        task_form = TaskForm(request.POST)

        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.save()

            return redirect('/ManagerProject')
    else:
        task_form = TaskForm()


    return render(request, 'Manager/manager_taskadd.html', {'task_form': task_form,'project': project})


def CreateTeam(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    project=Project.objects.filter(ManagerID=manager)
    employee=Employee.objects.all()
    
    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            task_id = team_form.cleaned_data['TaskID']
            # Check if a team already exists for the selected task
            existing_team = Team.objects.filter(TaskID=task_id).exists()
            if existing_team:
                # Handle the case where a team already exists for the task
                messages.error(request, 'A team already exists for the selected task.')
            else:
                team = team_form.save(commit=False)
                team.save()
                return redirect('/ManagerProject')
    else:
        team_form = TeamForm()

    context = {
        'manager': manager,
        'team_form': team_form,
        'project': project,
        'employee': employee,
    }

    return render(request, 'Manager/manager_teamadd.html', context)



def edit_project(request, project_id):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    project = Project.objects.get(ProjectID=project_id)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)

        if project_form.is_valid():
            project_form.save()
            next_url = request.GET.get('next')
            return redirect(next_url)
    else:
        project_form = ProjectForm(instance=project)
    return render(request, 'Manager/manager_projectadd.html', {'project_form': project_form,'manager':manager})

from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ManagerApp.models import Manager, Project, Task, Team, TeamMembers
from .forms import ProjectForm, TaskForm, TeamForm, TeamMembersForm

def edit_project(request, project_id):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")

    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")

    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(ProjectID=project_id)
    TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1)
    TeamFormSet = modelformset_factory(Team, form=TeamForm, extra=1)
    TeamMembersFormSet = modelformset_factory(TeamMembers, form=TeamMembersForm, extra=1)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        task_formset = TaskFormSet(request.POST, queryset=Task.objects.filter(ProjectID=project))
        team_formsets = [TeamFormSet(request.POST, queryset=Team.objects.filter(TaskID=task.TaskID)) for task in tasks]
        team_members_formsets = [TeamMembersFormSet(request.POST, queryset=TeamMembers.objects.filter(TeamID__in=Team.objects.filter(TaskID=task.TaskID))) for task in tasks]
        project_form.save()
        task_formset.save()
        for formset in team_formsets:
            formset.save()
        for formset in team_members_formsets:
            formset.save()
        return redirect('/ManagerDashboard')  # Redirect to dashboard or other appropriate page
    else:
        project_form = ProjectForm(instance=project)
        task_formset = TaskFormSet(queryset=Task.objects.filter(ProjectID=project))
        team_formsets = [TeamFormSet(queryset=Team.objects.filter(TaskID=task.TaskID)) for task in tasks]
        team_members_formsets = [TeamMembersFormSet(queryset=TeamMembers.objects.filter(TeamID__in=Team.objects.filter(TaskID=task.TaskID))) for task in tasks]

    return render(request, 'Manager/test.html', {
        'project_form': project_form,
        'task_formset': task_formset,
        'team_formsets': team_formsets,
        'team_members_formsets': team_members_formsets,
        'manager': manager
    })


def edit_task(request, task_id):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")

    try:
        # Assuming you have a way to retrieve the manager instance
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")

    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/ManagerDashboard')  # Redirect to dashboard or other appropriate page
    else:
        form = TaskForm(instance=task)

    return render(request, 'Manager/Manager_taskadd.html', {
        'task_form': form,
        'manager': manager
    })

def manager_leave(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    leaves = Leave.objects.all()
    form = LeaveForm()
    context = {'Leave': leaves, 'form': form, 'manager': manager,}
    return render(request, 'Manager/manager_leavetable.html', context)
    
    # return render(request, 'Manager/manager_leavetable.html',context)


def approve_leave(request, leave_id):
    leave = Leave.objects.get(LeaveID=leave_id)
    leave.Status = 'Approved'
    leave.save()
    return redirect('/leaverequest')   # Redirect to the same page to avoid form resubmission

def reject_leave(request, leave_id):
    leave = Leave.objects.get(LeaveID=leave_id)
    leave.Status = 'Rejected'
    leave.save()
    return redirect('/leaverequest')


def RecruitRequest(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    if request.method == 'POST':
        form = RecruitmentRequestForm(request.POST)
        if form.is_valid():
            recruitment_request = form.save(commit=False)
            recruitment_request.ManagerID = manager
            recruitment_request.save()
            form.save_m2m()
            return redirect('/ManagerDashboard')  # Redirect to a success page
    else:
        form = RecruitmentRequestForm()
        
    context = {
        'form': form,
        'manager': manager,
        
    }
    return render(request, 'Manager/recruit_request.html', context)





def job_application_view(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    # Query the manager based on the username
    try:
        manager = Manager.objects.get(Username=username)
    except Manager.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    # Fetch all JobApplication instances
    job_applications = JobApplication.objects.all()
    for job_application in job_applications:
        recruitment_applications = RecruitmentApplication.objects.filter(ApplicationID=job_application)
        applicants = [recruitment_application.ApplicantID for recruitment_application in recruitment_applications]
        job_application.applicants = applicants
    return render(request, 'Manager/jobsection.html',  {'job_applications': job_applications, 'manager': manager,})





# def CreateTask(request):
        
#         team_form = TeamForm(request.POST)
#         team_members_form = TeamMembersForm(request.POST)

#  team_form.is_valid() and team_members_form.is_valid():
#             task = task_form.save(commit=False)
#             task.ProjectID = project
#             task.save()
#             team = team_form.save(commit=False)
#             team.ProjectID = project
#             team.save()
#             team_members = team_members_form.save(commit=False)
#             team_members.TeamID = team
#             team_members.save()
            
            
            
#                     task_form = TaskForm()
#         team_form = TeamForm()
#         team_members_form = TeamMembersForm()
        
        
#         return render request(, 'team_form': team_form, 'team_members_form': team_members_form)
    
    
    