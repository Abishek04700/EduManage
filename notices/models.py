from django.conf import settings
from django.db import models


class Notice(models.Model):
    class Audience(models.TextChoices):
        ALL = 'ALL', 'Everyone'
        TEACHERS = 'TEACHERS', 'Teachers Only'
        STUDENTS = 'STUDENTS', 'Students Only'

    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.ALL)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
