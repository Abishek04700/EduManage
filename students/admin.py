from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'course', 'roll_number', 'status', 'admission_date')
    list_filter = ('course', 'status', 'gender')
    search_fields = ('admission_number', 'roll_number', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('user', 'course')
