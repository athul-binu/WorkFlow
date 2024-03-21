from django import forms
from .models import Attendance

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