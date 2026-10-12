from django.conf import settings
from django.db import models


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        GRADUATED = 'GRADUATED', 'Graduated'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile'
    )
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, blank=True)
    course = models.ForeignKey(
        'academics.Course', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='students'
    )
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.OTHER)
    admission_date = models.DateField(auto_now_add=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    guardian_email = models.EmailField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ['admission_number']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.admission_number})"
