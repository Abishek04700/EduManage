from django.conf import settings
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=150, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    joining_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.employee_id})"
