import os
import datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

import tagging
from image_cropping import ImageRatioField

from caching.caching_utils import cache_update, cache_evict
from utils.aux_utils import transliterate, get_image_path, produce_resized_image
from tradenplay.settings import THUMBNAIL_SIZE, IMG_UPLD_DIR

from .signal_processors import add_m2m_connections

class ActiveManager(models.Manager):

    "Base class's manager"

    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_active=True)
        
class FeaturedManager(models.Manager):

    def get_query_set(self):
        return super(FeaturedManager, self).get_query_set().filter(
            is_active=True).filter(is_featured=True)
    
    def all(self):
        return super(FeaturedManager, self).all().filter(
            is_active=True).filter(is_featured=True)
    
    def values(self):
        return super(FeaturedManager, self).values().filter(
            is_active=True).filter(is_featured=True)
            
            
class CatalogModelBase(models.Model):

    """
    Abstract base class for catalog models.
    """

    META_KWD_HELP_TEXT = mark_safe(_(
        """
        Comma delimited set of SEO keywords for meta tag.
        This one is rather important for SEO purposes.
        <br />
        The keyword propositions may
        be constructed as shown in the
        <a href="https://vimeo.com/32295368." style="font-size: 12px;">
            corresponding video
        </a>
        <br />
        At most cases should not  be longer than 5-7 words.
        """
    ))

    class Meta:
        abstract = True

    objects = models.Manager()  # default manager still operative
    active = ActiveManager()  # new manager for active items
    featured = FeaturedManager() # new manager for featured items
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,
                            unique=True,
                            help_text=_(
                                "Unique value, generated \
                                from name automatically.")
                            )
    description = models.TextField()

    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    image_url = models.CharField(max_length=255, editable=False, blank=True,
                                 null=True)
    thumbnail = models.ImageField(upload_to=get_image_path, blank=True,
                                  null=True)
    thumbnail_url = models.CharField(
        max_length=255, editable=False, blank=True,
        null=True)
    # https://github.com/jonasundderwolf/django-image-cropping
    cropping = ImageRatioField('image', '430x360') 
    
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    meta_keywords = models.CharField("Meta keywords", max_length=255,
                                     help_text=META_KWD_HELP_TEXT)
    meta_description = models.CharField("Meta description", max_length=255,
                                        help_text=_("Short(!) and relevant(!) \
                                                    description."))

    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    @property
    def cache_key(self):
        return self.get_absolute_url()

    def __unicode__(self):
        return self.name

    #"TODO: url buildout process requires further optimisation"
    def save(self, force_insert=False, force_update=False):
        newname = transliterate(self.name[0:20])
        if self.image:
            self.image_url = self.image.url

        if self.thumbnail:
            self.thumbnail_url = self.thumbnail.url
        elif self.image:
            dir, name = os.path.split(self.image.url)
            self.thumbnail_url = os.path.join(dir, 'thumbnail' + name)

        super(CatalogModelBase, self).save(force_insert, force_update)

        if not self.thumbnail and self.image:

                produce_resized_image(self.image,
                                      THUMBNAIL_SIZE,
                                      newname,
                                      'thumbnail')


# class ActiveCategoryManager(models.Manager):

    # def get_query_set(self):
        # return super(
            # ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class Category(CatalogModelBase):

    """
    Provides core structure of product catalog. Two self-pointing
    ManyToManyField 's  used, to provide multiple level nesting, as well as
    nesting a child category into several parents or making one parent have any
    number of children (and of any nesting level).
    """

    child_categories = models.ManyToManyField('self',
                                              symmetrical=False,
                                              related_name='child+',
                                              blank=True)
    parent_categories = models.ManyToManyField('self',
                                               symmetrical=False,
                                               related_name='parent+',
                                               blank=True)

    class Meta:

        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('catalog.views.show_category',
                       kwargs={'slug': self.slug})


    # def _create_connections(self, own_field, other_field):
        # for item in self.field.values('pk'):
            # object = self.objects.get(pk=item['pk'])
            # object.other_field.add(self)
            
    def save(self, force_insert=False, force_update=False):
        super(Category, self).save(force_insert, force_update)
        
        # for item in self.parent_categories.values('pk'):
            # object = self.__class__.objects.get(pk=item['pk'])
            # object.child_categories.add(self)
        
        # for item in self.child_categories.values('pk'):
            # object = self.__class__.objects.get(pk=item['pk'])
            # object.parent_categories.add(self)  
            
        

class Product(CatalogModelBase):

    
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                blank=True, null=True, default=Decimal('1.00'))
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True,
                                    default=Decimal('0.00'))
    is_bestseller = models.BooleanField(default=False)
    
    quantity = models.IntegerField(default="1")
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'products'
        ordering = ['created_at']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def cross_sells_hybrid(self):
        from checkout.models import Order, OrderItem
        from django.contrib.auth.models import User
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(Q(order__in=orders) |
                                         Q(order__user__in=users)).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), {'slug': self.slug})

try:
    tagging.register(Product)
except tagging.AlreadyRegistered:
    pass


class ActiveProductReviewManager(models.Manager):

    """
    Manager class to return only those
    product reviews where each instance is approved
    """

    def all(self):
        return super(
            ActiveProductReviewManager, self).all().filter(is_approved=True)


class ProductReview(models.Model):

    RATINGS = ((5, 5), (4, 4), (3, 3), (2, 2), (1, 1))

    objects = models.Manager()
    approved = ActiveProductReviewManager()

    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()


post_save.connect(cache_update, sender=Product)
post_delete.connect(cache_evict, sender=Product)
post_save.connect(cache_update, sender=Category)
post_save.connect(add_m2m_connections, sender=Category)
post_delete.connect(cache_evict, sender=Category)
