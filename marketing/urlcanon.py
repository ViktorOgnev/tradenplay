from django.http import get_host, HttpResponsePermanentRedirect
from tradenplay import settings


class URLCanonicalizationMiddleware(object):

    def process_views(self, request, view_func, view_args, view_kwargs):

        protocol = "https://" if request.is_sequre() else "http://"
        host = get_host(request)
        new_url = ''
        url = ''.join([
            protocol,
            settings.CANONICAL_URL_HOST,
            request.get_full_path()
        ])
        try:
            if host in settings.CANONICAL_URLS_TO_REWRITE:
                new_url = url
        except AttributeError:
            if host != settings.CANONICAL_URL_HOST:
                new_url = url
        return HttpResponsePermanentRedirect(new_url)
