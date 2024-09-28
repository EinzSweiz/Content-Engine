from django.contrib import admin
from .models import Project, ProjectUser

class ProjectUserInline(admin.TabularInline):
    model = ProjectUser
    raw_id_fields = ['user']
    extra = 0
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'timestamp', 'updated']
    search_fields = ('title', 'owner')
    list_filter = ['active', 'timestamp']
    inlines = [ProjectUserInline, ]
    # prepopulated_fields = {'handle': ('title', )}