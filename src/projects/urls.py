from django.urls import path
from . import views
app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='project_list'),
    path('create/', views.project_create_view, name='project_create'),
    path('<slug:handle>/', views.project_detail_update_view, name='project_update'),
    path('delete/<slug:handle>/', views.project_delete_view, name='project_delete'),
    path('activate/<slug:handle>/', views.activate_project_view, name='project-activate'),
    path('deactivate/<slug:handle>/', views.deactivate_project_view, name='project-deactivate'),

]