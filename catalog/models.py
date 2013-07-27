import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.aux_utils import get_image_path
from decimal import Decimal
from tradenplay.settings import MEDIA_ROOT_URL

class Category(models.Model):   
        
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, 
        help_text=_("""Unique value, generated from name automatically."""))
    
    image = models.ImageField(upload_to=get_image_path, blank=True,  
                                     null=True)
    image_url = models.CharField(max_length=255, editable=False, blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta keywords", max_length=255,
        help_text = "Comma delimited set of SEO keywords for meta tag")
    
    meta_description = models.CharField("Meta description", max_length=255,
        help_text= "Content for description meta tag")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    child_categories = models.ManyToManyField('self', symmetrical=False, 
        related_name='child+', blank=True)
    parent_categories = models.ManyToManyField('self', symmetrical=False,
        related_name='parent+', blank=True)
    
    class Meta:
        
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __unicode__(self):
        return self.name
    
    
    def save(self, force_insert=False, force_update=False):
        self.image_url = MEDIA_ROOT_URL + self.image.url.split(MEDIA_ROOT_URL)[1]
        
        super(Category, self).save(force_insert, force_update)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('catalog.views.show_category', kwargs={'slug': self.slug})
        
        
        
class Product(models.Model):
        
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=50, unique=True, 
        help_text="""Unique value, generated from name automatically.""")
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                blank=True, null=True, default=Decimal('1.00'))
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True,
                                    default=Decimal('0.00'))
    image = models.ImageField(upload_to=get_image_path, blank=True,null=True)
    image_url = models.CharField(max_length=255, editable=False, blank=True,
                                 null=True)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    quantity = models.IntegerField()
    description = models.TextField()
    
    
    meta_keywords = models.CharField("Meta keywords", max_length=255,
        help_text = "Comma delimited set of SEO keywords for meta tag")
    
    meta_description = models.CharField("Meta description", max_length=255,
        help_text= "Content for description meta tag")
   
    
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    
    categories = models.ManyToManyField(Category)
    
    class Meta:
        db_table = 'products'
        ordering = ['created_at']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        
    def __unicode__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False):
        self.image_url = MEDIA_ROOT_URL + self.image.url.split(MEDIA_ROOT_URL)[1]
        super(Product, self).save(force_insert, force_update)
    
    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), {'slug': self.slug})
    
    
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
    
    