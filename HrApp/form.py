from django import forms
from .models import Applicant,RecruitmentApplication,JobApplication
class ApplicantForm(forms.ModelForm):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    FirstName = forms.CharField(label='First Name',required=True)
    LastName = forms.CharField(label='Last Name',required=True)
    Email = forms.EmailField(label='Email',required=True)
    PhoneNumber = forms.CharField(label='Phone Number',required=True)
    Resume = forms.FileField(label='Resume',required=True)
    ProficiencyLevel = forms.ChoiceField(choices=PROFICIENCY_CHOICES, label='Proficiency Level',required=True)

    class Meta:
        model = Applicant
        fields = ['FirstName', 'LastName', 'Email', 'PhoneNumber', 'Resume', 'ProficiencyLevel']
        widgets = {
            'FirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'LastName': forms.TextInput(attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'PhoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'Resume': forms.FileInput(attrs={'class': 'form-control'}),
            'ProficiencyLevel': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        
        



class RecruitmentApplicationForm(forms.ModelForm):
    ApplicationDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'form-control'}))
    ApplicationID = forms.ModelChoiceField(queryset=JobApplication.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    Status_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved')
    ]
    Status = forms.ChoiceField(choices=Status_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = RecruitmentApplication
        fields = ['ApplicationID', 'ApplicationDate', 'Status']
        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ApplicationID'].queryset = JobApplication.objects.all()
        self.fields['ApplicationID'].empty_label = None
