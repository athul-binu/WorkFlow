from django import forms
from .models import Attendance,Leave

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['EmployeeID', 'Status']
        widgets = {
            'EmployeeID': forms.HiddenInput(),
            'Status': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EmployeeID'].required = False
        self.fields['Status'].required = False
        
class LeaveForm(forms.ModelForm):
    LEAVE_TYPE_CHOICES = (
        ('Sick Leave', 'Sick Leave'),
        ('Vacation Leave', 'Vacation Leave'),
        ('Maternity Leave', 'Maternity Leave'),
        # Add more choices as needed
    )

    LeaveType = forms.ChoiceField(choices=LEAVE_TYPE_CHOICES, required=False)

    class Meta:
        model = Leave
        fields = ['LeaveType', 'StartDate', 'EndDate', 'Duration', 'Comments']
        labels = {
            'LeaveType': 'Leave Type',
            'StartDate': 'Start Date',
            'EndDate': 'End Date',
            'Duration': 'Duration',
            # 'Status': 'Status',
            'Comments': 'Comments'
        }

        widgets = {
            'StartDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Start Date'}),
            'EndDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'End Date'}),
            'Duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in days'}),
            # 'Status': forms.Select(attrs={'class': 'form-control'}),
            'Comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comments'}),
        }
