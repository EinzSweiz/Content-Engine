from django.urls import path 
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.item_list_view, name='item_list'),
    path('<int:id>/', views.item_detail_view, name='item_detail'), 
    path('delete/<int:id>/', views.item_delete_view, name='item_delete'),
    path('create/', views.item_create_view, name='item_create'),
]