from django.db import models


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text="e.g. 2025-2026")
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """A class / grade / cohort, e.g. 'Grade 10 - A'."""

    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10, blank=True)
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name='courses'
    )
    class_teacher = models.ForeignKey(
        'teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='classes_led'
    )

    class Meta:
        ordering = ['name', 'section']
        unique_together = ('name', 'section', 'academic_year')

    def __str__(self):
        label = f"{self.name} {self.section}".strip()
        return f"{label} ({self.academic_year})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(
        'teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='subjects'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
