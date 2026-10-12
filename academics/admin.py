from django.contrib import admin

from .models import AcademicYear, Course, Subject


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_current')
    list_filter = ('is_current',)


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'academic_year', 'class_teacher')
    list_filter = ('academic_year',)
    search_fields = ('name', 'section')
    inlines = [SubjectInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course', 'teacher')
    search_fields = ('name', 'code')
    list_filter = ('course',)
