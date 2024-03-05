from django.db import models
from ManagerApp.models import Manager
from EmployeeApp.models import Employee

class Admin(models.Model):
    AdminID = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='profilepics/', null=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.EmailField()
    PhoneNumber = models.CharField(max_length=15)
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"


class RemovalRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    ManagerID = models.ForeignKey(Manager, on_delete=models.CASCADE)
    TargetUserID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    RequestDate = models.DateTimeField()
    Status = models.CharField(max_length=100)
    Comments = models.TextField()

    class Meta:
        db_table = 'removal_request'

    def __str__(self):
        return f"Request ID: {self.RequestID}"


class AdminEmployeeRemovalLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    AdminID = models.ForeignKey(Admin, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    RemovalReason = models.TextField()
    RemovalDate = models.DateTimeField()

    class Meta:
        db_table = 'admin_employee_removal_log'

    def __str__(self):
        return f"Log ID: {self.LogID}"


class AdminManagerRemovalLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    AdminID = models.ForeignKey(Admin, on_delete=models.CASCADE)
    ManagerID = models.ForeignKey(Manager, on_delete=models.CASCADE)
    RemovalReason = models.TextField()
    RemovalDate = models.DateTimeField()

    class Meta:
        db_table = 'admin_manager_removal_log'

    def __str__(self):
        return f"Log ID: {self.LogID}"


class AdminActionLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    AdminID = models.ForeignKey(Admin, on_delete=models.CASCADE)
    ActionDescription = models.TextField()
    ActionDate = models.DateTimeField()

    class Meta:
        db_table = 'admin_action_log'

    def __str__(self):
        return f"Log ID: {self.LogID}"
