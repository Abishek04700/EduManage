
from django import forms

from accounts.models import User
from .models import Student


class StudentUserForm(forms.ModelForm):
    """Creates or updates the underlying User account for a student."""

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep the existing password."
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'profile_photo',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT

        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)
        elif not user.pk:
            user.set_unusable_password()

        if commit:
            user.save()

        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'admission_number',
            'roll_number',
            'course',
            'gender',
            'guardian_name',
            'guardian_phone',
            'guardian_email',
            'status',
        ]

    def __init__(self, *args, is_staff_user=False, **kwargs):
        super().__init__(*args, **kwargs)

        # Students can edit personal and guardian details only.
        # Admins and teachers can edit all profile fields.
        if not is_staff_user:
            restricted_fields = [
                'admission_number',
                'roll_number',
                'course',
                'status',
            ]

            for field in restricted_fields:
                self.fields.pop(field, None)
