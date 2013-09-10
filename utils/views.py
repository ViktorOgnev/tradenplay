from tradenplay.settings import ASKBOT_URL
from django.views.defaults import server_error
from django.views.defaults import page_not_found


def view_500(request):
    if not request.path.startswith('/' + ASKBOT_URL):
        template_name = 'errors/500.html'
    else:
        template_name = '500.html'

    return server_error(request, template_name=template_name)

def view_404(request):
    if not request.path.startswith('/' + ASKBOT_URL):
        template_name = 'errors/404.html'
    else:
        template_name = '404.html'
    
    return page_not_found(request, template_name=template_name)