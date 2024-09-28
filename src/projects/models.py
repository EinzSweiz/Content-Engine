from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from cfehome.utils.generators import unique_slugify
from django.urls import reverse
from . import validator
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class AnonymousProject():
    value = None
    is_activated = False

class ProjectUser(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)


class ProjectQuerySet(models.QuerySet):
    def has_access(self, user=None):
        if user == None:
            return self.none()
        return self.filter(
            Q(owner=user) |
            Q(projectuser__user=user,
              projectuser__active=True)
        )
    
class ProjectManager(models.Manager):
    def get_queryset(self):
        return  ProjectQuerySet(self.model, using=self._db)
    def has_access(self, user=None):
        return self.get_queryset().has_access(user=user)
class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_projects')
    users = models.ManyToManyField(User, blank=True, related_name='projects', through=ProjectUser)
    title = models.CharField(max_length=120, null=True, blank=True)
    handle = models.SlugField(null=True, blank=True, unique=True,
                            validators=[validator.validate_project_handle])
    description = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_added')
    added_by_username = models.CharField(max_length=120, null=True, blank=True)
    last_modified_by = models.ForeignKey(User, related_name='projects_changed', on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = ProjectManager()

    def get_delete_url(self):
        return reverse('projects:project_delete', kwargs={'handle': self.handle})

    def get_absolute_url(self):
        return reverse('projects:project_update', kwargs={'handle': self.handle})
    
    def get_activate_url(self):
        return reverse('projects:project-activate', kwargs={'handle': self.handle})
    
    def get_prefix(self, trailing_slash=True):
        if trailing_slash:
            return f'projects/{self.id}/'
        return f'projects/{self.id}'    
    
    @property
    def is_activated(self):
        return True
    
    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        if self.added_by:
            self.added_by_username = self.added_by.username
        if not self.handle:
            self.handle = unique_slugify(self, slug_field='handle', invalid_slug='create')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

