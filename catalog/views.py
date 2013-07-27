from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from catalog.models import Category, Product
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from catalog.forms import ProductAddToCartForm
from cart import cart_utils
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf


def index(request, template_name="catalog/index.html"):
    page_title = _('This is an online store title')
    return render_to_response(template_name, locals(), 
                              context_instance=RequestContext(request))
    
def show_category(request, slug, template_name="catalog/category.html"):
    category = get_object_or_404(Category, slug=slug)
    products = category.product_set.all()
    page_title = category.name
    meta_keywords = category.meta_keywords
    meta_description = category.meta_description
    
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# New product view with get/post detection 
# It could be a good idea to rewrite it later as a class based view
def show_product(request, slug, template_name="catalog/product.html"):
    
    product = get_object_or_404(Product, slug=slug)
    categories = product.categories.all()
    page_title = product.name
    meta_keywords = product.meta_keywords
    meta_description = product.meta_description
    
    # What's the method?
    if request.method == 'POST':
        # Add the bound form to cart_create
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # Check if posted data is valid
        if form.is_valid():
            # Add to cart and redirect to cart page
            cart_utils.add_to_cart(request)
            # If test cookie worked, get rid of it 
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(reverse('show_cart'))
            
    else:
        # It's a get, create and unbound form. Note request is a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # Assign a hidden input to a product slug
    form.fields['slug'].widget.attrs['value'] = slug
    # Set the test cookie on a first GET request 
    request.session.set_test_cookie()
    context = locals()
    context.update(csrf(request))
    
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))