from django.db import models
from ManagerApp.models import *



class Skill(models.Model):
    SkillID = models.AutoField(primary_key=True)
    SkillName = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Skill'

    def __str__(self):
        return self.SkillName
    

class Designation(models.Model):
    DesignationID = models.AutoField(primary_key=True)
    DesignationTitle = models.CharField(max_length=100)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Designation'

    def __str__(self):
        return self.DesignationTitle


class Department(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=100)

    class Meta:
        db_table = 'Department'

    def __str__(self):
        return self.DepartmentName


class Employee(models.Model):
    EmployeeID = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='profilepics/', null=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.EmailField()
    PhoneNumber = models.CharField(max_length=15)
    DOB = models.DateField()
    HireDate = models.DateTimeField()
    BasicSalary = models.DecimalField(max_digits=10, decimal_places=2)
    DesignationID = models.ForeignKey(Designation, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE)
    SkillID = models.ManyToManyField(Skill)

    class Meta:
        db_table = 'Employee'

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"


class Leave(models.Model):
    LeaveID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    LeaveType = models.CharField(max_length=100)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    Duration = models.DecimalField(max_digits=5, decimal_places=2)
    Status = models.CharField(max_length=100)
    Comments = models.TextField()

    class Meta:
        db_table = 'Leave'

    def __str__(self):
        return f"Leave ID: {self.LeaveID}, Employee: {self.EmployeeID}"


class Attendance(models.Model):
    AttendanceID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Date = models.DateTimeField()
    TotalHours = models.TimeField()
    Status = models.CharField(max_length=100)

    class Meta:
        db_table = 'Attendance'

    def __str__(self):
        return f"Attendance ID: {self.AttendanceID}, Employee: {self.EmployeeID}"