from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'catalog.views.index',
        {'template_name': 'catalog/index.html'}, 
        name='catalog_home'),
        
    url(r'^category/(?P<slug>[-\w]+)/$', 'catalog.views.show_category', 
        {'template_name': 'catalog/category.html'},
        name='catalog_category'),
    
    url(r'^product/(?P<slug>[-\w]+)/$', 'catalog.views.show_product', 
        {'template_name': 'catalog/product.html'},
        name='catalog_product'),
       
    #(r'^tag_cloud/$', 'tag_cloud', 
       #{'template_name': 'catalog/tag_cloud.html'}, 'tag_cloud'),
    #(r'^tag/(?P<tag>[-\w]+)/$', 'tag', 
      # {'template_name': 'catalog/tag.html'}, 'tag'),
    #(r'^review/product/add/$', 'add_review', {}, 'add_product_review'),
    #(r'^tag/product/add/$', 'add_tag'),
)