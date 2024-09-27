from django.urls import reverse


def site_urls(request):
    project_create_url = reverse('projects:project_create')
    handle = request.session.get('project_handle')
    deactivate_project = reverse('projects:project-deactivate', kwargs={'handle': handle}) if handle else None
    items_create_url = reverse('items:item_create')
    item_list_url = reverse('items:item_list')
    return {
        'home_url': reverse('landing:home'),
        'about_url': reverse('landing:about'),
        'project_create': project_create_url,
        'projects_create': project_create_url,
        'deactivate_project_url': deactivate_project,
        'deactivate_url': deactivate_project,
        'item_create_url': items_create_url,
        'item_list_url': item_list_url,
    }