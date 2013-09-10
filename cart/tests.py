import httplib

from django.test import TestCase, Client
from django.core import urlresolvers
from django.db import IntegrityError
from django.core.context_processors import csrf
from django.conf import settings

from catalog.models import Product
from catalog.forms import ProductAddToCartForm
from .models import CartItem
from . import cart_utils

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class CartTestCase(TestCase):
    
    fixtures = ['catalog_initial_data.json']
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.product = Product.active.all()[0]
    
    def _get_product_response(self, postdata=None):
        product_url = self.product.get_absolute_url()
        return self.client.post(product_url, postdata)
    
    def test_cart_id(self):
        home_url = urlresolvers.reverse('catalog_home')
        self.client.get(home_url)
        # Check that there is cart id set in the session after a page with cart
        # box has been requested.
        self.failUnless(self.client.session.get(cart_utils.CART_ID_SESSION_KEY, ''))
    
    def test_add_product(self):
        QUANTITY = 3
        
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, httplib.OK)
        
        # Store count in cart count variable.
        cart_item_count = self.get_cart_item_count()
        # Assert that the cart item count is 0.
        self.failUnlessEqual(cart_item_count, 0)
        
        # Send POST request to add to cart.
        cookie = self.client.cookies[settings.SESSION_COOKIE_NAME]
        csrf_token = response.context['csrf_token']
        postdata = {'product_slug': self.product.slug, 
                    'quantity': QUANTITY,
                    'csrfmiddlewaretoken':csrf_token,
                    'submit': 'Update'
                    }
        response = self._get_product_response(postdata)
        
        # Assert redirected to cart page - 302 then 200.
        cart_url = urlresolvers.reverse('show_cart')
        self.assertRedirects(response, cart_url, status_code=httplib.FOUND, 
                             target_status_code=httplib.OK)
        
        # Assert cart item count is incremented by one
        self.assertEqual(self.get_cart_item_count(), cart_item_count + 1)
        cart_id = self.get_cart_id()
        last_item = CartItem.objects.filter(cart_id=cart_id).latest('date_added')
        # Assert the latest cart item has a quantity of QUANTITY.
        self.failUnlessEqual(last_item.quantity, QUANTITY)
        # Assert the latest cart item is the correct product.        
        self.failUnlessEqual(last_item.product, self.product)
        
    
    def get_cart_item_count(self):
        cart_id = self.get_cart_id()
        return CartItem.objects.filter(cart_id=cart_id).count()        
        
    def get_cart_id(self):
        return self.client.session.get(cart_utils.CART_ID_SESSION_KEY)
        
    def test_add_product_empty_quantity(self):
        postdata = {'product_slug': self.product.slug,
                    'quantity': ''}
        response = response = self._get_product_response(postdata)
        expected_error = unicode(
            ProductAddToCartForm.base_fields['quantity'].error_messages['required'])
        self.assertFormError(response, "form", "quantity", [expected_error])
        
    def test_add_to_cart_fails_csrf(self):
        """ 
        adding product fails without including 
        the CSRF token to POST request parameters
        """
        quantity = 2
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, httplib.OK )
        
        # perform the post of adding to the cart
        postdata = {'product_slug': self.product.slug, 
                    'quantity': quantity }
        response = self._get_product_response(postdata )
        
        # assert forbidden error due to missing CSRF input
        self.assertEqual(response.status_code, httplib.FORBIDDEN )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        