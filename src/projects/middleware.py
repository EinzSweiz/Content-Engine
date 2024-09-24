from .models import Project
from django.core.cache import cache
from .models import AnonymousProject

class ProjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        if not hasattr(request, 'project'):
            request.project = AnonymousProject()
            if request.user.is_authenticated:
                print(request.session.get('project_handle'))
                project_handle = request.session.get('project_handle')
                project_object = None
                cache_str = None
                if project_handle is not None:
                    cache_str = f'_project_handle_cache_{project_handle}'
                    project_object = cache.get(cache_str)
                if project_object is None and project_handle is not None:   
                    try:
                        project_object = Project.objects.filter(handle=project_handle).first()
                    except:
                        pass
                if project_object is not None:
                    cache.set(cache_str, project_object)
                    request.project = project_object
        return self.get_response(request)