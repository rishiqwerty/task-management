from django.contrib import admin

from .models import Task, PromptResponse
admin.site.register(Task)
admin.site.register(PromptResponse)