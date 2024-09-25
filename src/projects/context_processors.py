from .models import Project

def user_projects_context(request):
    qs = Project.objects.none()
    if request.user.is_authenticated:
        qs = Project.objects.filter(owner=request.user)
    return {
        'project_list': qs,
    }