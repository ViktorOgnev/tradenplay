from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from checkout import checkout_utils

from .cart_utils import  get_cart_items, cart_distinct_item_count, \
    get_cart_subtotal, remove_from_cart, update_cart


def show_cart(request, template_name="cart/cart.html"):
    
    
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            remove_from_cart(request)
        if postdata['submit'] == 'Update':
            update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout_utils.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
        
    cart_items = get_cart_items(request)
    
    cart_item_count = cart_distinct_item_count(request)
    page_title = _('Shopping Cart')
    cart_subtotal = get_cart_subtotal(request)
    context = locals()
    
    context.update(csrf(request))
    
    return render_to_response(template_name, context, RequestContext(request))
                              


                              