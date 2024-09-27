from .models import Project
from . import cache as projects_cache
def user_projects_context(request):
    username = None
    project_qs = Project.objects.none()
    if request.user.is_authenticated:
        username = request.user.username
        project_qs = projects_cache.get_user_projects(username=username)
    return {
        'project_list': project_qs,
    }