from django_htmx.http import trigger_client_event
from django.http import HttpResponse

def render_refresh_list_view(request, response_text=""):
    custom_refresh_event = 'refresh_list_view'
    reponse = HttpResponse('Created')
    return trigger_client_event(reponse, custom_refresh_event)