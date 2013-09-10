from tradenplay import settings
from django.contrib.sites.models import Site


def project_constants(HttpRequest):
    site_name = Site.objects.get(id=settings.SITE_ID)
    return {'STATIC_URL': settings.STATIC_URL,
            'IMG_UPLD_DIR': settings.IMG_UPLD_DIR,
            'site_name': site_name
            }
