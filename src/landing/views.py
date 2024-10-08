from django.shortcuts import render
from items.models import Item
from projects.decorators import project_required


@project_required
def dashboard_view(request):
    return render(request, 'dashboard/home.html', {})

def home_page_view(request):
    if not request.user.is_authenticated:
        return render(request, 'landing/home.html', {})
    return dashboard_view(request)


def about_page_view(request):
    print(request.project)
    return render(request, 'landing/about.html', {})
