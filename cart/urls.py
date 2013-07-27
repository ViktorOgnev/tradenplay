from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('cart.views',
    url(r'^$', 'show_cart', {'template_name':'cart/cart.html'}, name='show_cart'),
)
