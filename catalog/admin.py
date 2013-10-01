from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE

from solo.admin import SingletonModelAdmin

from .models import Category, Product, ProductReview, HomepageSeoText, Brand
from .forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):

    form = ProductAdminForm

    list_display = ('name', 'price', 'brand',
                    'old_price', 'created_at', 'updated_at', )
    list_per_page = 50
    ordering = ['brand', 'name']
    search_fields = [
        'name', 'description', 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Basic data'), {
            'fields': ('name', 'brand', 'price', 'quantity', 'description',
                       'categories', 'image', 'thumbnail', 'meta_keywords',
                       'meta_description'),
            'classes': ('wide', 'extrapretty')
        }),
        (_('Advanced data'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ('sku', 'is_bestseller', 'is_featured', 'is_active',
                       'slug', 'created_at', 'updated_at',)
        }),
    )
    filter_horizontal = ['categories']

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }

    class Media:
        js = ['js/admin/display_thumbs.js',
              '/static/admin/js/tiny_django_browser.js']


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'created_at', 'updated_at', )
    list_per_page = 30
    ordering = ['name']
    search_fields = [
        'name', 'description', 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['child_categories', 'parent_categories']


admin.site.register(Category, CategoryAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user', 'content', 'title']

admin.site.register(ProductReview, ProductReviewAdmin)

# class HomepageSeoTextAdmin(SingletonModelAdmin, admin.ModelAdmin):
    # list_display = ('seo_text',)

admin.site.register(HomepageSeoText, SingletonModelAdmin)


class BrandAdmin(admin.ModelAdmin):

    search_fields = ['name']
    list_display = ('name', 'pk', 'offsite_url', 'logo')

admin.site.register(Brand, BrandAdmin)
