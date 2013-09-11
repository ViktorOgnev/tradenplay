"""
main url configuration file for the site
"""
from django.conf import settings
from django.conf.urls.defaults import handler404
from django.conf.urls.defaults import handler500
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

if getattr(settings, 'ASKBOT_MULTILINGUAL', False) == True:
    from django.conf.urls.i18n import i18n_patterns
    urlpatterns = i18n_patterns('',
                               (r'%s' %
                                settings.ASKBOT_URL, include('askbot.urls'))
                                )
else:
    urlpatterns = patterns('',
                          (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
                           )

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    # (r'^cache/', include('keyedcache.urls')), - broken views disable for now
    url(r'^catalog/', include('catalog.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^checkout/', include('checkout.urls')),
    (r'^settings/', include('askbot.deps.livesettings.urls')),
    (r'^followit/', include('followit.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', include('robots.urls')),
    url(  # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\', '/')},
    ),
    url(r'^accounts/', include('accounts.urls')),
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^search/', include('search.urls')),
    url(r'', include('marketing.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^rosetta/', include('rosetta.urls')),
                            )

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler500 = 'utils.views.view_500'
handler404 = 'utils.views.view_404'
