from django import forms
from ManagerApp.models import Project, Task, Team, TeamMembers
from EmployeeApp.models import Skill
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['ProjectName', 'Description', 'Status', 'Priority', 'StartDate', 'DueDate']

class TaskForm(forms.ModelForm):
    SkillID = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Task
        fields = ['ProjectID','Title', 'Description','SkillID']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['TaskID','TeamName', 'TeamLead']

class TeamMembersForm(forms.ModelForm):
    class Meta:
        model = TeamMembers
        fields = ['EmployeeID', 'Role']
