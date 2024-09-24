from django.shortcuts import render, redirect
from .models import Project
from django.contrib import messages

def delete_project_from_session(request):
    try:
        del request.session['project_handle']
    except:
        pass

def activate_project_view(request, handle=None):
    try:
        project_object = Project.objects.filter(owner=request.user, handle=handle)
    except:
        project_object = None
        print('not here')
    if project_object is None:
        delete_project_from_session(request)
        messages.error(request, 'Project could not activate. Try again')
        return redirect('/projects')
    request.session['project_handle'] = handle
    messages.success(request, 'Project activated.')
    return redirect('/')

def deactivate_project_view(request, handle=None):
    delete_project_from_session(request)
    messages.success(request, 'Project Deactivated.')
    return redirect('/')