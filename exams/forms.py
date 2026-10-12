from django import forms

from .models import Exam, Result


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'course', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks_obtained', 'max_marks', 'remarks']
