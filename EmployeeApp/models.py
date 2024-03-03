from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.department_name

class Designation(models.Model):
    designation_id = models.AutoField(primary_key=True)
    designation_title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'designation'

    def __str__(self):
        return self.designation_title

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'skill'

    def __str__(self):
        return self.skill_name

class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'manager'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    dob = models.DateField()
    hire_date = models.DateTimeField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    comments = models.TextField()

    class Meta:
        db_table = 'task'

    def __str__(self):
        return self.title

class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    comments = models.TextField()

    class Meta:
        db_table = 'leave'

    def __str__(self):
        return self.leave_type

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    total_hours = models.TimeField()
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'attendance'

    def __str__(self):
        return f"{self.employee} - {self.date}"

class TeamMember(models.Model):
    team_member_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_member'

    def __str__(self):
        return f"{self.team_name} - {self.employee}"

class RecruitmentRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    hr_id = models.IntegerField()
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    open_date = models.DateTimeField()
    close_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    recruitment_type = models.CharField(max_length=100)
    request_date = models.DateTimeField()
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recruitment_request'

    def __str__(self):
        return self.job_title

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total_days = models.TimeField()
    pay_period = models.DateTimeField()
    overtime = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_status = models.CharField(max_length=100)

    class Meta:
        db_table = 'payroll'

    def __str__(self):
        return f"Payroll for {self.employee}"
