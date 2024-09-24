from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from cfehome.utils.generators import unique_slugify
User = settings.AUTH_USER_MODEL

class AnonymousProject():
    value = None
    is_activated = False

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120, null=True, blank=True)
    handle = models.SlugField(null=True, blank=True, unique=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


    @property
    def is_activated(self):
        return True
    
    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = unique_slugify(self, slug_field='handle')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

