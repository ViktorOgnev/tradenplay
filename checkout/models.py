from django.db import models

from django import forms
from django.contrib.auth.models import User
from catalog.models import Product
from django.utils.translation import ugettext_lazy as _
from utils.aux_utils import make_hash


class BaseOrderInfo(models.Model):

    class Meta:
        abstract = True

    # Contact info
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=25)

    # Shipping informaiton
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50, blank=True)
    shipping_state = models.CharField(max_length=50, blank=True)
    shipping_country = models.CharField(max_length=50, blank=True)
    shipping_zip = models.CharField(max_length=10, blank=True)

    # Billing Information
    billing_name = models.CharField(max_length=50, blank=True)
    billing_address_1 = models.CharField(max_length=50, blank=True)
    billing_address_2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=50, blank=True)
    billing_state = models.CharField(max_length=50, blank=True)
    billing_country = models.CharField(max_length=50, blank=True)
    billing_zip = models.CharField(max_length=10, blank=True)


class Order(BaseOrderInfo):

    # Status options
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    # Set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (SHIPPED, 'Shipped'),
                      (CANCELLED, 'Cancelled'),)

    # Order information
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField(editable=False)
    user = models.ForeignKey(User)
    transaction_id = models.CharField(max_length=20)

    # Order displayable identifier
    number = models.CharField(max_length=50, editable=False)

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    class Meta:
        db_table = 'orders'
        ordering = ['-date']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __unicode__(self):
        return _('Order number') + str(self.id)

    def save(self, force_insert=False, force_update=False):

        order_hash = make_hash(str(self.id), self.user.name)
        self.number = order_hash.split(',')[1][0:8]

        super(Order, self).save(force_insert, force_update)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('order_details', kwargs={'order_id': self.id})


class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order)

    @property
    def total(self):
        return sefl.quantity * sefl.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    class Meta:
        db_table = 'order_items'
        ordering = ['order', 'product']
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __unicode__(self):
        return sefl.product.name + ' (' + self.product.sku + ')'

    def get_absolute_url(self):
        return self.product.get_absolute_url()
