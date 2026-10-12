from django.contrib import admin

from .models import Exam, Result


class ResultInline(admin.TabularInline):
    model = Result
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'start_date', 'end_date')
    list_filter = ('course',)
    inlines = [ResultInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks_obtained', 'max_marks')
    list_filter = ('exam', 'subject')
    search_fields = ('student__admission_number',)
