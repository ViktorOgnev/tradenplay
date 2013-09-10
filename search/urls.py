from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('search.views',
    url(r'^results/$', 'results', {'template_name': 'search/results.html'},
        name='search_results')
    )