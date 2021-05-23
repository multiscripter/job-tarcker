from django.contrib import admin

from job_tracker.models.action import Action
from job_tracker.models.task import Task


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ['id', 'text']
    ordering = ['text']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('job_day', 'name', 'time', 'id')
    list_display_links = ['id', 'name']
    ordering = ['job_day', 'id']


admin.site.register(Action, ActionAdmin)
admin.site.register(Task, TaskAdmin)
