from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'posted_by', 'is_pinned', 'created_at')
    list_filter = ('audience', 'is_pinned')
    search_fields = ('title', 'content')
