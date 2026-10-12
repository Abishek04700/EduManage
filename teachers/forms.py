from django import forms

from accounts.models import User

from .models import Teacher


class TeacherUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep unchanged")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'profile_photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.TEACHER
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        elif not user.pk:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['employee_id', 'qualification', 'specialization', 'joining_date', 'salary']
        widgets = {'joining_date': forms.DateInput(attrs={'type': 'date'})}
