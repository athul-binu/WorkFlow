from django import forms
from ManagerApp.models import Project, Task, Team, TeamMembers,RecruitmentRequest
from EmployeeApp.models import Skill,Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import HiddenInput
from HrApp.models import HR
class ProjectForm(forms.ModelForm):
    StartDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    DueDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Project
        fields = ['ProjectName','ProjectLead', 'Description', 'Status', 'Priority', 'StartDate', 'DueDate']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class TaskForm(forms.ModelForm):
    SkillID = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Task    
        fields = ['ProjectID','Title', 'Description','SkillID']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['TaskID','TeamName', 'TeamLead']

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class TeamMembersForm(forms.ModelForm):
    EmployeeID = Employee.objects.all()
    class Meta:
        model = TeamMembers
        fields = ['TeamID', 'EmployeeID', 'Role']


    def __init__(self, *args, **kwargs):
        super(TeamMembersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        
        
        


class RecruitmentRequestForm(forms.ModelForm):
    SkillID = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    HRID = forms.ModelChoiceField(queryset=HR.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = RecruitmentRequest
        fields = ['HRID','JobTitle', 'TaskDescription', 'CloseDate', 'Status', 'RecruitmentType', 'Experience', 'SkillID']
        widgets = {
            'CloseDate': forms.DateInput(attrs={'type': 'date','class': 'form-control'}), 
            'JobTitle': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'TaskDescription': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'Status': forms.TextInput(attrs={'class': 'form-control'}),
            'RecruitmentType': forms.TextInput(attrs={'class': 'form-control'}),
            'Experience': forms.TextInput(attrs={'class': 'form-control'}),
            'HRID': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
