from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'timestamp', 'updated']
    search_fields = ('title', 'owner')
    list_filter = ['active', 'timestamp']
    # prepopulated_fields = {'handle': ('title', )}