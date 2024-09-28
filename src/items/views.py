from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from . import forms
# from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required as login_required
from .models import Item
from projects.decorators import project_required
from cfehome import http
from django.http import QueryDict, HttpResponse, JsonResponse
from cfehome.env import config
import s3
import pathlib
import mimetypes
import boto3
from django_htmx.http import HttpResponseClientRedirect

AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID', cast=str)
AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY', cast=str)
AWS_BUCKET_NAME=config('AWS_BUCKET_NAME', cast=str)


@project_required
@login_required
def item_upload_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    template_name = 'items/upload.html'
    prefix = instance.get_prefix()
    if request.htmx:
        template_name = 'items/snippets/upload.html'
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        client = s3.S3Client(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            default_bucket_name=AWS_BUCKET_NAME,
            region_name='eu-north-1'
        ).client
        if not prefix.endswith('/'):
            prefix += '/'
        file_path = f'{prefix}{file.name}'
        try:
            client.upload_fileobj(file, AWS_BUCKET_NAME, file_path)
            return JsonResponse({'message': 'File uploaded successfully!'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    return render(request, template_name, {'instance': instance})

@project_required
@login_required
def item_files_delete_view(request, id=None, name=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if not request.htmx:
        detail_url = instance.get_absolute_url
        return redirect(detail_url)
    if  request.method != 'POST':
        detail_url = instance.get_absolute_url
        return HttpResponseClientRedirect(detail_url)
    prefix = instance.get_prefix()
    client = s3.S3Client(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        default_bucket_name=AWS_BUCKET_NAME,
        region_name='eu-north-1',
    ).client
    prefix = instance.get_prefix()
    key = f'{prefix}{name}'
    if key.endswith('/'):
        key = key[:-1]
    client.delete_object(Bucket=AWS_BUCKET_NAME, Key=key)
    return HttpResponse(f'{name} Deleted')

@project_required
@login_required
def item_files_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if not request.htmx:
        detail_url = instance.get_absolute_url
        return redirect(detail_url)
    template_name = 'items/snippets/object_table.html'
    prefix = instance.get_prefix()
    client = s3.S3Client(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        default_bucket_name=AWS_BUCKET_NAME,
        region_name='eu-north-1',
    ).client
    paginator = client.get_paginator('list_objects_v2')
    pag_gen = paginator.paginate(Bucket=AWS_BUCKET_NAME, Prefix=prefix)
    object_list = []
    for page in pag_gen:
        for c in page.get('Contents', []):
            key = c.get('Key')
            size = c.get('Size')
            name = pathlib.Path(key).name
            if size == 0:
                continue
            _type = None
            try:
                _type = mimetypes.guess_type(name)[0]
            except:
                pass
            is_image = 'image' in str(_type)
            url = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': AWS_BUCKET_NAME,
                    'Key': key,
                },
                ExpiresIn=36000,
            )
            download_url = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': AWS_BUCKET_NAME,
                    'Key': key,
                    'ResponseContentDisposition': f'attachment; filename="{name}"'
                },
                ExpiresIn=3600,
            )
            updated = c.get('LastModified')
            data = {
                'key': key,
                'size': size,
                'updated': updated,
                'type': _type,
                'is_image': is_image,
                'name': pathlib.Path(key).name,
                'download_url': download_url,
                'url': url,
            }
            object_list.append(data)
    return render(request, template_name, {
        'object_list':object_list,
        'instance':instance,
        })


@project_required
@login_required
def item_delete_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if request.method == 'POST':
        instance.delete()
        if request.htmx:
            return http.render_refresh_list_view(request)
        return redirect('items:item_delete')
    return render(request, 'items/delete.html', {'instance':instance})

@project_required
@login_required
def item_list_view(request):
    object_list = Item.objects.filter(project=request.project)
    template_name = 'items/list.html'
    if request.htmx:
        template_name = 'items/snippets/table.html'
    return render(request, template_name, {'object_list': object_list})

@project_required
@login_required
def item_detail_update_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    form = forms.ItemUpdateForm(request.POST or None, instance=instance)
    if form.is_valid():
        item_object = form.save(commit=False)
        item_object.last_modified_by = request.user
        item_object.save()
        return redirect(item_object.get_absolute_url())
    else:
        print(form.errors)
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, 'items/detail.html', context)

@project_required
@login_required
def item_detail_edit_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if not request.htmx:
        detail_url = instance.get_absolute_url
        return redirect(detail_url)
    template_name = 'items/snippets/table-raw-edit.html'
    success_name = 'items/snippets/table-raw.html'
    if f'{request.method}'.lower() == 'patch':
        print(request.body)
        query_dict = QueryDict(request.body)
        data = query_dict.dict()
        form = forms.ItemPatcheForm(data)
        if form.is_valid():
            valid_data = form.cleaned_data
            for k, v in valid_data.items():
                if v == "":
                    continue
                if not v:
                    continue
                setattr(instance, k, v)
            instance.save()
        choices = Item.ItemStatus.choices
        template_name = success_name
        context = {
            'instance': instance,
            'choices': choices,
            'form':form,
        }
        return render(request, template_name, context)
    form = forms.ItemEditForm(request.POST or None, instance=instance)
    if form.is_valid():
        item_object = form.save(commit=False)
        item_object.last_modified_by = request.user
        item_object.save()
        template_name = success_name
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, template_name, context)
@project_required
@login_required
def item_create_view(request):
    template_name = 'items/create.html'
    if request.htmx:
        template_name = 'items/snippets/forms.html'
    form = forms.ItemCreateForm(request.POST or None)
    if form.is_valid():
        item_object = form.save(commit=False)
        item_object.project = request.project
        item_object.added_by = request.user
        item_object.save()
        if request.htmx:
            return http.render_refresh_list_view(request)
        return redirect(item_object.get_absolute_url())
    item_create_url = reverse('items:item_create')
    context = {
        'form': form,
        'btn_label': 'Create',
        'action_url': item_create_url
    }

    return render(request, template_name, context)