import httplib
from decimal import Decimal

from django.test import TestCase, Client
from django.core import urlresolvers
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import IntegrityError

from .models import Category, Product, ProductReview
from .forms import ProductAddToCartForm


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class NewUserTestCase(TestCase):
    
    fixtures = ['catalog_initial_data.json']

    def setUp(self):
        self.client = Client()
        logged_in = self.client.session.has_key(SESSION_KEY)
        self.assertFalse(logged_in)

    def _get_template_name(self, url):
        "Get template name kwarg for a given url."
        url_entry = urlresolvers.resolve(url)
        return url_entry[2]['template_name']

    def test_items_exist(self):
        self.assertTrue(Product.objects.all().count > 0)
        self.assertTrue(Category.objects.all().count > 0)

    def test_view_homepage(self):
        Site.objects.create(domain='foo.com', name='foo.com')
        home_url = urlresolvers.reverse('catalog_home')
        response = self.client.get(home_url)
        # Check that we did a response.
        self.failUnless(response)
        # Check that status code of response was success.
        # (httplib.OK = 200)
        self.assertEqual(response.status_code, httplib.OK)

    def test_view_category(self):
        category = Category.objects.all()[0]
        category_url = category.get_absolute_url()
        # Get the template_name arg from URL entry.
        template_name = self._get_template_name(category_url)
        # Test category page load.
        response = self.client.get(category_url)
        # Test if there is a response.
        self.failUnless(response)
        # Test that http status code is OK.
        self.assertEqual(response.status_code, httplib.OK)
        # Test that the template is used in a response.
        self.assertTemplateUsed(response, template_name)
        # Test that category page contains category information.
        self.assertContains(response, category.name)
        #self.assertContains(response, category.get_absolute_url())
        

    def test_view_product(self):
        product = Product.active.all()[0]
        product_url = product.get_absolute_url()
        template_name = self._get_template_name(product_url)
        response = self.client.get(product_url)
        self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, product.name)
        self.assertContains(response, product.description)
        # Check for cart form in product page response.
        cart_form = response.context['form']
        self.failUnless(cart_form)
        # Check that cart form is an instance of the correct form class.
        self.failUnless(isinstance(cart_form, ProductAddToCartForm))
        # Test if the product reviews variable is there.
        product_reviews = response.context[0].get('product_reviews', None)
        self.failIfEqual(product_reviews, None)


class ActiveProductManagerTestCase(NewUserTestCase):
    
    
        
    def test_inactive_product_returns_404(self):
        """
        Access an inactive product and check a response
        from its get_absolute_url method.
        """
        inactive_product = Product.objects.filter(is_active=False)[0]

        inactive_product_url = inactive_product.get_absolute_url()
        # Load the template file used to render the product page.
        template_name = self._get_template_name(inactive_product_url)
        response = self.client.get(inactive_product_url)
        self.assertTemplateUsed(response, "errors/404.html")
        self.assertTemplateNotUsed(response, template_name)


class ProductTestCase(TestCase):
    
    fixtures = ['catalog_initial_data.json']
    
    def setUp(self):
        self.product = Product.active.all()[0]
        self.product.price = Decimal('134.57')
        self.product.save()
        self.client = Client()

    def test_sale_price(self):
        self.product.old_price = Decimal('234.56')
        self.product.save()
        self.failIfEqual(self.product.sale_price(), None)
        self.assertEqual(self.product.sale_price(), self.product.price)

    def test_no_sale_price(self):
        self.product.old_price = Decimal('0.00')
        self.product.save()
        self.failUnlessEqual(self.product.sale_price(), None)

    def test_permalink(self):
        url = self.product.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)

    def test_unicode(self):
        self.assertEqual(self.product.__unicode__(), self.product.name)


class CategoryTestCase(TestCase):
    
    fixtures = ['catalog_initial_data.json']
    
    def setUp(self):
        self.category = Category.active.all()[0]
        self.client = Client()

    def test_permalink(self):
        url = self.category.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.failUnlessEqual(response.status_code, httplib.OK)

    def test_unicode(self):
        self.assertEqual(self.category.__unicode__(), self.category.name)


class ProductReviewTestCase(TestCase):
    
    fixtures = ['catalog_initial_data.json', 'accounts_initial_data.json',
                'askbot_initial_data.json']
    
    def test_orphaned_product_review(self):
        product_review = ProductReview()
        self.assertRaises(IntegrityError, product_review.save())

    def test_product_review_defaults(self):
        user = User.objects.all()[0]
        product = Product.active.all()[0]
        product_review = ProductReview(user=user, product=product)
        product_review.save()
        for field in pr._meta.fields:
            if field.has_default():
                self.assertEqual(pr.__dict__[field.name], field.default)
        