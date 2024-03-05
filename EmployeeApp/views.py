from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ProjectForm, TaskForm, TeamForm, TeamMembersForm
from ManagerApp.models import Manager, Project, Task, Team, TeamMembers

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        try:
            manager = Manager.objects.get(Username=username)
        except Manager.DoesNotExist:
            return HttpResponse("User does not exist")

        if role == 'admin':
            if password == manager.Password:
                # Set session data
                request.session['username'] = username
                print("Session exists:", 'user' in request.session)
                request.session['role'] = role
                return redirect('admin_dashboard')  
            else:
                return HttpResponse("Invalid password")
        elif role == 'manager':
            if password == manager.Password:
                # Set session data
                request.session['username'] = username
                print("Session exists:", 'user' in request.session)
                request.session['role'] = role
                return redirect('/ManagerDashboard')  # Adjust the URL name as per your project
            else:
                return HttpResponse("Invalid password")
        elif role == 'employee':
            # Assuming you have an 'employee_dashboard' named URL pattern
            request.session['username'] = username
            request.session['role'] = role
            return redirect('employee_dashboard')  # Adjust the URL name as per your project
        elif role == 'hr':
            # Assuming you have an 'hr_dashboard' named URL pattern
            request.session['username'] = username
            request.session['role'] = role
            return redirect('hr_dashboard')  # Adjust the URL name as per your project
        else:
            # Invalid role
            return HttpResponse("Invalid role")
    return render(request, 'login.html')

def logout_view(request):
    # Clear session data
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

    
    # Initialize empty lists to store task and team data
    task_data = []
    team_data = []
    
    # Iterate through each project to retrieve associated tasks and teams
    for project in projects:
        tasks = Task.objects.filter(ProjectID=project.ProjectID)
        print(project.ProjectID)
        print("below stask")
        print(tasks)
        for task in tasks:
            # Retrieve teams associated with the current task
            teams = Team.objects.filter(TaskID=task.TaskID)
            print(teams)
            print(teams)
            # Extend the team_data list with teams
            team_data.extend(teams)
            print(team_data)
        # Extend the task_data list with tasks
        task_data.extend(tasks)
        print(task_data)
    
    # Prepare the context to pass to the template
    context = {
        'manager': manager,
        'projects': projects,
        'task_data': task_data,
        'team_data': team_data,
    }
    print("Projects:", projects)
    print("Task Data:", task_data)
    print("Team Data:", team_data)

    return render(request, "Manager/manager_dashboard.html", context)






def project_overview(request, project_id):
    # Retrieve project details
    project = Project.objects.get(ProjectID=project_id)

    # Retrieve tasks related to the project
    tasks = Task.objects.filter(ProjectID=project)

    # Retrieve team related to the project
    team = Team.objects.get(ProjectID=project)

    # Retrieve team members related to the team
    team_members = TeamMembers.objects.filter(TeamID=team)

    context = {
        'project': project,
        'tasks': tasks,
        'team': team,
        'team_members': team_members
    }

    return render(request, 'employee_project.html', context)

def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        task_form = TaskForm(request.POST)
        team_form = TeamForm(request.POST)
        team_members_form = TeamMembersForm(request.POST)

        if project_form.is_valid() and task_form.is_valid() and team_form.is_valid() and team_members_form.is_valid():
            project = project_form.save()
            task = task_form.save(commit=False)
            task.ProjectID = project
            task.save()
            team = team_form.save(commit=False)
            team.ProjectID = project
            team.save()
            team_members = team_members_form.save(commit=False)
            team_members.TeamID = team
            team_members.save()
            return redirect('project_overview', project_id=project.id)
    else:
        project_form = ProjectForm()
        task_form = TaskForm()
        team_form = TeamForm()
        team_members_form = TeamMembersForm()

    return render(request, 'Manager/manager_projectadd.html', {'project_form': project_form, 'task_form': task_form, 'team_form': team_form, 'team_members_form': team_members_form})
