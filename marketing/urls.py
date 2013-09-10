from django.conf.urls.defaults import patterns, url
from .sitemap import SITEMAPS


urlpatterns = patterns('marketing.views',
    url(r'^robots\.txt$', 'robots', name='marketing_robots'),
)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': SITEMAPS},
        name='marketing_sitemap'),
)


