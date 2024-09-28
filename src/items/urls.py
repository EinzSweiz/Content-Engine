from django.urls import path, re_path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.item_list_view, name='item_list'),
    path('<int:id>/', views.item_detail_update_view, name='item_detail'),
    path('<int:id>/upload/', views.item_upload_view, name='item_upload'),
    path('<int:id>/edit', views.item_detail_edit_view, name='edit'),  
    path('<int:id>/files', views.item_files_view, name='files'),  
    re_path(r'^(?P<id>\d+)/files/(?P<name>.*)$', views.item_files_delete_view, name='files_delete'),  
    path('delete/<int:id>/', views.item_delete_view, name='item_delete'),
    path('create/', views.item_create_view, name='item_create'),
]