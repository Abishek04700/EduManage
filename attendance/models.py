from django.conf import settings
from django.db import models


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'
        EXCUSED = 'EXCUSED', 'Excused'

    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, related_name='attendance_records'
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ['-date']
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"
