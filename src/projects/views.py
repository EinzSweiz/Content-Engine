from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required as login_required
from . import forms
from django.http import Http404


PROJECT_CAN_DELETE_ITEM_THRESHOLD = 2

@login_required
def project_list_view(request):
    object_list = Project.objects.has_access(request.user)
    return render(request, 'projects/list.html', {'object_list': object_list})


def get_project_or_404(request, handle=None, skip404=False):
    object_list = Project.objects.filter(handle=handle).has_access(request.user)
    if not object_list.exists() and not skip404:
        raise Http404
    if not object_list.exists() and skip404:
        return None
    return object_list.first()

@login_required
def project_detail_update_view(request, handle=None):
    instance = get_project_or_404(request, handle=handle)
    form = forms.ProjectUpdateForm(request.POST or None, instance=instance)
    items_qs = instance.item_set.all()

    if form.is_valid():
        project_object = form.save(commit=False)
        project_object.last_modified_by = request.user
        project_object.save()
        return redirect('projects:project_list')
    context = {
        'form': form,
        'instance': instance,
        'item_qs': items_qs
    }
    return render(request, 'projects/detail.html', context)
    

@login_required
def project_delete_view(request, handle=None):
    instance = get_project_or_404(request, handle=handle)
    items_qs = instance.item_set.all()
    item_count = items_qs.count()
    items_exists = items_qs.exists()
    if request.method == 'POST':
        if items_exists and item_count >= PROJECT_CAN_DELETE_ITEM_THRESHOLD:
            messages.error(request, 'Can not delete project with 2 and more active items')
            return redirect(instance.get_delete_url())
        instance.delete()
        return redirect('projects:project_list')
    return render(request, 'projects/delete.html')


@login_required
def project_create_view(request):
    # if not request.project.is_activated:
    #     return render(request, 'projects/activate.html', {})
    form = forms.ProjectCreateForm(request.POST or None)
    if form.is_valid():
        project_object = form.save(commit=False)
        project_object.owner = request.user
        project_object.save()
        return redirect('projects:project_list')
    context = {
        'form': form
    }
    return render(request, 'projects/create.html', context)

def delete_project_from_session(request):
    try:
        del request.session['project_handle']
    except:
        pass

def activate_project_view(request, handle=None):
    project_object = get_project_or_404(request, handle=handle, skip404=True)
    if project_object is None:
        delete_project_from_session(request)
        messages.error(request, 'Project could not activate. Try again')
        return redirect('/projects')
    request.session['project_handle'] = handle
    messages.success(request, 'Project activated.')
    return redirect('landing:home')

def deactivate_project_view(request, handle=None):
    delete_project_from_session(request)
    messages.error(request, 'Project Deactivated.')
    return redirect('landing:home')