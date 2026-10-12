from django import forms

from academics.models import Course

from .models import Attendance


class AttendanceFilterForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'remarks']
