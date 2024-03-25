from django.db import models
from EmployeeApp.models import Department

class HR(models.Model):
    HRID = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='profilepics/', null=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.EmailField()
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15)
    HireDate = models.DateTimeField()
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE)
    Role = models.CharField(max_length=100)

    class Meta:
        db_table = 'hr'

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"


class Applicant(models.Model):
    ApplicantID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.EmailField()
    PhoneNumber = models.CharField(max_length=15)
    Resume = models.FileField()
    ProficiencyLevel = models.CharField(max_length=100)

    class Meta:
        db_table = 'applicant'

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"


class JobApplication(models.Model):
    ApplicationID = models.AutoField(primary_key=True)
    RequestID = models.ForeignKey('ManagerApp.RecruitmentRequest', on_delete=models.CASCADE)
    JobDescription = models.CharField(max_length=100)
    OpenDate = models.DateField()
    CloseDate = models.DateField()
    Status = models.CharField(max_length=100)

    class Meta:
        db_table = 'job_application'

    def __str__(self):
        return self.JobDescription


class RecruitmentApplication(models.Model):
    RecruitmentApplicationID = models.AutoField(primary_key=True)
    ApplicationID = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    ApplicantID = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    ApplicationDate = models.DateTimeField()
    Status = models.CharField(max_length=100)

    class Meta:
        db_table = 'recruitment_application'

    def __str__(self):
        return f"Application ID: {self.ApplicationID}, Applicant ID: {self.ApplicantID}"















class PerformanceReview(models.Model):
    ReviewID = models.AutoField(primary_key=True)
    RecruitmentApplicationID = models.ForeignKey(RecruitmentApplication, on_delete=models.CASCADE)
    ReviewDate = models.DateTimeField()
    ReviewerID = models.ForeignKey(HR, on_delete=models.CASCADE)
    Rating = models.IntegerField()
    Comments = models.TextField()

    class Meta:
        db_table = 'performance_review'

    def __str__(self):
        return f"Review ID: {self.ReviewID}, Rating: {self.Rating}"
