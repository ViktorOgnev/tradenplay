from tradenplay.settings import ASKBOT_URL
from django.views.defaults import page_not_found

def view_500(request):
    if not request.path.startswith('/' + ASKBOT_URL):
        template_name = 'errors/500.html'
    else:
        template_name = '500.html'

    return page_not_found(request, template_name=template_name)