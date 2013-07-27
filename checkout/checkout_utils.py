from cart import cart_utils 
from checkout.models import Order, OrderItem
from checkout.forms import CheckoutForm
from checkout import authnet
from tradenplay import settings
from django.core import urlresolvers
import urllib
from django.utils.translation import ugettext_lazy as _


def get_checkout_url(request):
    """
    Return the URL from the checkout URL for cart
    """
    return urlresolvers.reverse('checkout')

def process(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    
    postdata = request.POST.copy()
    card_num = postdata.get('credit_card_number', '')
    exp_month = postdata.get('credit_card_expire_month', '')
    exp_year = postdata.get('cedit_card_expire_year', '')
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv', '')
    amount = cart_utils.cart_subtotal(request)
    results = {}
    response = authnet.do_auth_capture(amount=amount,
                                       card_num=card_num,
                                       exp_date=exp_date,
                                       card_cvv=cvv)
                                       
    if response[0] == APPROVED:
        transacion_id = response[6]
        order = create_order(request, transaction_id)
        results = {'order_number': order.id, 'message':''}
    if response[0] == DECLINED:
        results = {'order_number': 0, 
                   'message': _('There is a problem with your credit card')}
    if respose[0] == ERROR:
        results = {'order_number': 0, 
                   'message': _('There was en error processing your order')}
    return results
    
    def create_order(request, transaction_id):
        order = Order()
        checkout_form = CheckoutForm(request.POST, instance=order)
        order = checkout_form.save(commit=False)
        order.transaction_id = transaction_id
        order.ip_address = reqest.META.get('REMOTE_ADDR')
        order.user = None
        order.status = Order.SUBMITTED
        order.save()
        
        # If order save succeeded
        if order.pk:
            cart_items = cart_utils.get_cart_items(request)
            for ci in cart_items:
                # Create order item for each cart item
                oi = OrderItem()
                oi.order = order
                oi.quantity = ci.quantity
                oi.price = ci.price
                oi.product = ci.product 
                oi.save()
            # Now we can emty the cart
            cart_utils.empty_cart(request)
        # Return  the new order object
        return order 