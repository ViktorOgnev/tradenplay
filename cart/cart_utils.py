import decimal
import random
from string import ascii_letters
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Max

from tradenplay.settings import SESSION_AGE_DAYS
from catalog.models import Product
from .models import CartItem
CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """
    Get the current user's cart id, sets new one if blank.
    """
    if not CART_ID_SESSION_KEY in request.session:
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    cart_id = ''
    cart_id_length = 50
    for counter in range(cart_id_length):
        cart_id += ascii_letters[random.randint(0, len(ascii_letters) - 1)]
    return cart_id
    

def get_cart_items(request):
    """
    Return all items frm the current user's cart
    """
    return CartItem.objects.filter(cart_id=_cart_id(request))
    

def add_to_cart(request):
    """
    Add item to cart
    """
    postdata = request.POST.copy()
    
    # Get product slug from postdatam, return blank if empty(the second
    # parameter for get() )
    product_slug = postdata.get('slug', '')
    
    # Get quantity added, return 1 if empty
    quantity = postdata.get('quantity', 1)
    
    # Fetch a product or return a missing page error
    p = get_object_or_404(Product, slug=product_slug)
    
    # Get products in cart
    cart_products = get_cart_items(request)
    product_in_cart = False
    
    # Check to see if item is already in cart 
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            
            # Update the quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:
        
        # Create and save a new cart item.
        cart_item = CartItem()
        cart_item.product = p
        cart_item.quantity =  quantity
        cart_item.cart_id = _cart_id(request)
        cart_item.save()
    
    
def cart_distinct_item_count(request):
    return get_cart_items(request).count()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def update_cart(request):
    """
    Update quantity for a single item
    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)
    
    
def remove_from_cart(request):
    """
    Remove a single item from cart
    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def get_cart_subtotal(request):
    """
    Gets the total cost for a current cart 
    """
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total
    
    
def cart_is_empty(request):
    return cart_distinct_item_count(request) == 0
    
    
def empty_the_cart(request):
    user_cart = get_cart_items(request)
    user_cart.delete()
    
    
def remove_old_cart_items():
    print "Removing old carts."
    # Calculate date of SESSION_AGE_DAYS ago.
    remove_before = datetime.now() + timedata(days=-SESSION_AGE_DAYS)
    cart_ids = []
    # Get all the old cart items.
    old_items = CartItem.objects.values('cart_id').annotate(
        last_change=Max('date_added')).filter(last_change_lt=remove_before
                                              ).order_by()
    # Create a list of cart id's that haven't been modified.
    for item in old_items:
        cart_ids.append(item['cart_id'])
    # Get obsolette itemse b id and remove them.
    to_remove = CartItem.objects.filter(cart_id__in=cart_ids)
    to_remove.delete()
    print str(len(cart_ids)) + "carts were removed."
