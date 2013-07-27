from django.contrib import admin
from catalog.models import Category, Product
from catalog.forms import ProductAdminForm

class ProductAdmin(admin.ModelAdmin):
    
    form = ProductAdminForm
    
    list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at', )
    list_per_page = 50
    ordering = ['brand', 'name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug' : ('name',)}
    
admin.site.register(Product, ProductAdmin)
 
 
class CategoryAdmin(admin.ModelAdmin):  
    
    list_display = ('name', 'created_at', 'updated_at', )
    list_per_page = 30
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug' : ('name',)}
    
admin.site.register(Category, CategoryAdmin)
 