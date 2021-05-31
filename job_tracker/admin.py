from django.contrib import admin

from job_tracker.models.task import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('job_day', 'name', 'time', 'id')
    list_display_links = ['id', 'name']
    ordering = ['-job_day', 'id']
    fields = ('name', 'job_day', 'time', 'actions')


admin.site.register(Task, TaskAdmin)
