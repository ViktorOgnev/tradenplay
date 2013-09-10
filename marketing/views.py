import os
from django.http import HttpResponse
from tradenplay.settings import PROJECT_ROOT

ROBOTS_PATH = os.path.join(PROJECT_ROOT, 'marketing/robots.txt')


def robots(request):
    return HttpResponseRedirect(open(ROBOTS_PATH).read(), 'text/plain')
