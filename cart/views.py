from django.shortcuts import render_to_response
from django.template import RequestContext
from checkout import checkout_utils
from django.utils.translation import ugettext_lazy as _
import cart_utils 
from django.http import HttpResponseRedirect

def show_cart(request, template_name="cart/cart.html"):
    
    
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout_utils.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
        
    cart_items = cart_utils.get_cart_items(request)
    
    cart_item_count = cart_utils.cart_distinct_item_count(request)
    page_title = _('Shopping Cart')
    cart_subtotal = cart_utils.cart_subtotal(request)
    
    return render_to_response(template_name, locals(), RequestContext(request))
                              


                              