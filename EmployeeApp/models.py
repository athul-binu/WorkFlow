from django.db import models

class Skill(models.Model):
    SkillID = models.AutoField(primary_key=True)
    SkillName = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Skill'

    def __str__(self):
        return self.SkillName
    


class Department(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=100)

    class Meta:
        db_table = 'Department'

    def __str__(self):
        return self.DepartmentName


class Designation(models.Model):
    DesignationID = models.AutoField(primary_key=True)
    DesignationTitle = models.CharField(max_length=100)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Designation'

    def __str__(self):
        return self.DesignationTitle


class Employee(models.Model):
    EmployeeID = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='profilepics/', null=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Username = models.CharField(max_length=100,null=True,unique=True)
    Password = models.CharField(max_length=100,null=True)
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
    Status = models.CharField(max_length=100,null=True,blank=True)
    Comments = models.TextField()

    class Meta:
        db_table = 'Leave'

    def __str__(self):
        return f"Leave ID: {self.LeaveID}, Employee: {self.EmployeeID}"


class Attendance(models.Model):
    AttendanceID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Date = models.DateTimeField()
    TotalHours = models.TimeField(null=True)
    Status = models.CharField(max_length=100,null=True, blank=True)

    class Meta:
        db_table = 'Attendance'

    def __str__(self):
        return f" Date: {self.Date}, Employee: {self.EmployeeID}"
class Payroll(models.Model):
    PayrollID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Salary = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentDate = models.DateField()

    class Meta:
        db_table = 'payroll'

    def __str__(self):
        return f"Payroll ID: {self.PayrollID}, Employee: {self.EmployeeID}"
    
    
    
class Event(models.Model):
    EventID = models.AutoField(primary_key=True)
    ManagerID = models.ForeignKey('ManagerApp.Manager',on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    EventName = models.CharField(max_length=100)
    EventDescription = models.TextField()
    EventPriority = models.CharField(max_length=100)
    EventDate = models.DateTimeField()
    
    
    class Meta:
        db_table='Event'
    def __str__(self):
        return f"Event Name: {self.EventName}"
    
class ScheduledEvent(models.Model):
    ScheduledEventID = models.AutoField(primary_key=True)
    ManagerID = models.ForeignKey('ManagerApp.Manager',on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    ScheduledEventName = models.CharField(max_length=255)
    ScheduledEventDescription = models.CharField(max_length=255,null=True)
    ScheduledEventPriority = models.CharField(max_length=255)
    ScheduledEventDate = models.DateTimeField()
    
    class Meta:
        db_table="ScheduledEvent"
        
        
    def __str__(self):
        return f"Scheduled Name: {self.ScheduledEventName}"
    