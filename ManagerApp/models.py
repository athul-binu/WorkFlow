from django.db import models
from EmployeeApp.models import Skill, Department, Designation
from HrApp.models import HR

class RecruitmentRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    HRID = models.ForeignKey(HR, on_delete=models.CASCADE)
    ManagerID = models.ForeignKey('Manager', on_delete=models.CASCADE)
    JobTitle = models.CharField(max_length=100)
    TaskDescription = models.TextField()
    CloseDate = models.DateField()
    Status = models.CharField(max_length=100)
    RecruitmentType = models.CharField(max_length=100)
    Experience = models.CharField(max_length=100)
    SkillID = models.ManyToManyField(Skill)

    class Meta:
        db_table = 'recruitment_request'

    def __str__(self):
        return self.JobTitle

class Manager(models.Model):
    ManagerID = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='profilepics/', null=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.EmailField()
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15)
    HireDate = models.DateTimeField()
    DesignationID = models.ForeignKey(Designation, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'manager'

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

class Project(models.Model):
    ProjectID = models.AutoField(primary_key=True)
    ProjectName = models.CharField(max_length=100)
    ProjectLead=models.ForeignKey('EmployeeApp.Employee',on_delete=models.CASCADE,null=True)
    ManagerID = models.ForeignKey(Manager, on_delete=models.CASCADE)
    Description = models.TextField()
    Status = models.CharField(max_length=100,null=True)
    Priority = models.CharField(max_length=100,null=True)
    StartDate = models.DateField(null=True)
    DueDate = models.DateField(null=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.ProjectName


class Task(models.Model):
    TaskID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Project, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    SkillID = models.ManyToManyField(Skill)

    class Meta:
        db_table = 'task'

    def __str__(self):
        return self.Title


class Team(models.Model):
    TeamID = models.AutoField(primary_key=True)
    TeamName = models.CharField(max_length=100)
    TeamLead = models.ForeignKey('EmployeeApp.Employee', on_delete=models.CASCADE)
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team'

    def __str__(self):
        return self.TeamName


class TeamMembers(models.Model):
    TeamMemberID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey('EmployeeApp.Employee', on_delete=models.CASCADE)
    Role = models.CharField(max_length=100)
    TeamID = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_members'

    def __str__(self):
        return f"{self.EmployeeID.FirstName} {self.EmployeeID.LastName}"
