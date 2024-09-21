from . import views 
from django.urls import path

app_name = 'landing'

urlpatterns = [
    path('', views.home_page_view, name='home')
]