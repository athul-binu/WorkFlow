from django.contrib import admin
from EmployeeApp.models import Employee, Leave, Attendance, Payroll, Skill, Department, Designation,Event,ScheduledEvent
from ManagerApp.models import Manager, Project, Task, Team, TeamMembers, RecruitmentRequest
from HrApp.models import HR, Applicant, JobApplication, RecruitmentApplication, PerformanceReview
from AdminApp.models import Admin, RemovalRequest, AdminEmployeeRemovalLog, AdminManagerRemovalLog, AdminActionLog

# Register EmployeeApp models
admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(Payroll)
admin.site.register(Skill)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Event)
admin.site.register(ScheduledEvent)
# Register ManagerApp models
admin.site.register(Manager)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(TeamMembers)
admin.site.register(RecruitmentRequest)

# Register HrApp models
admin.site.register(HR)
admin.site.register(Applicant)
admin.site.register(JobApplication)
admin.site.register(RecruitmentApplication)


# Register AdminApp models
admin.site.register(Admin)
admin.site.register(RemovalRequest)
admin.site.register(AdminEmployeeRemovalLog)
admin.site.register(AdminManagerRemovalLog)
admin.site.register(AdminActionLog)
