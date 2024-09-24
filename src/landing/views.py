from django.shortcuts import render


def home_page_view(request):
    print(request.project.is_activated)
    return render(request, 'landing/home.html', {})


def about_page_view(request):
    print(request.project)
    return render(request, 'landing/about.html', {})
