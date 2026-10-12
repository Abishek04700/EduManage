from django import forms

from .models import AcademicYear, Course, Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'section', 'academic_year', 'class_teacher']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'course', 'teacher']


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['name', 'is_current']
