from django.conf.urls.defaults import patterns, url
from tradenplay import settings

urlpatterns = patterns('accounts.views',
    url(r'^register/$', 'register',
        {'template_name': 'registration/register.html',
         'SSL':settings.ENABLE_SSL},
        name='register'),
    url(r'^logout/$', 'log_out', 
    name='accounts_log_out'),
    url(r'^login/$', 'log_in', 
        name='accounts_log_in'),
    url(r'^my_account/$', 'my_account',
        {'template_name': 'registration/my_account.html'},
        name='my_account'),
    url(r'order_details/(?P<order_id>[-\w]+)/$', 'order_details',
        {'template_name': 'registration/order_details.html'},
        name='order_details'),
    url(r'order_info/$', 'order_info', 
        {'template_name': 'registration/register.html'},
        name='order_info'),
        
)

# urlpatterns += patterns('django.contrib.auth.views',
    # url(r'^login/$', 'login', 
        # {'template_name': 'registration/login.html', 'SSL':settings.ENABLE_SSL},
        # name='accounts_login'),
# )