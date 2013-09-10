from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('catalog.views',
    url(r'^$', 'index',
        {'template_name': 'catalog/index.html'}, 
        name='catalog_home'),
        
    url(r'^category/(?P<slug>[-\w]+)/$', 'show_category', 
        {'template_name': 'catalog/category.html'},
        name='catalog_category'),
    
    url(r'^product/(?P<slug>[-\w]+)/$', 'show_product', 
        {'template_name': 'catalog/product.html'},
        name='catalog_product'),
       
    url(r'^tag_cloud/$', 'tag_cloud', 
        {'template_name': 'catalog/tag_cloud.html'},
        name='ctalog_tag_cloud'),
        
    url(r'^tag/(?P<tag>[-\w]+)/$', 'tag', 
        {'template_name': 'catalog/tag.html'},
        name='catalog_tag'),
        
    url(r'^review/product/add/$', 'add_review',{},
        name='catalog_product_add_review'),
        
    url(r'^tag/product/add/$', 'add_tag',
        name='catalog_product_add_tag'),
)