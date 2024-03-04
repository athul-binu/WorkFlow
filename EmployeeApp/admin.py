from django.contrib import admin

# Register your models here.
# admin/admin.py

from django.contrib import admin
# from .models import AdminActionLog, AdminEmployeeRemovalLog, AdminManagerRemovalLog
from EmployeeApp.models import Employee, Leave, Attendance,Payroll, RecruitmentRequest,Manager, Project, Task, Team, TeamMembers,Skill,Department,Designation

# admin.site.register(AdminActionLog)
# admin.site.register(AdminEmployeeRemovalLog)
# admin.site.register(AdminManagerRemovalLog)

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(Payroll)
admin.site.register(Skill)
admin.site.register(Department)
admin.site.register(Designation)
# admin.site.register(HR)
admin.site.register(RecruitmentRequest)

admin.site.register(Manager)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(TeamMembers)
