from django.contrib.flatpages.models import FlatPage
from django import template
from django.core.cache import cache

from tradenplay.settings import CACHE_TIMEOUT
from cart import cart_utils
from catalog.models import Category

register = template.Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart_utils.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count}

@register.inclusion_tag("tags/footer.html")
def footer_links():
    flatpage_list = FlatPage.objects.all()
    return {'flatpage_list': flatpage_list}

@register.inclusion_tag("tags/product_list.html")
def product_list(products, header_text):
    return {"products": products,
            "header_text": header_text}




@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    """
    Represent a nested category strucure in django-template-friendly manner
    
    """
    list_cache_key = 'active_category_link_list'
    active_categories = cache.get(list_cache_key)
    if not active_categories:
        category_structure_list = _generate_category_list()
        cache.set(list_cache_key, active_categories, CACHE_TIMEOUT)
    return {
        'category_structure_list': category_structure_list,
        'request_path': request_path
    }
    
#"TODO: add simple caching"
def _generate_item_list(input_list, result=None):
    """
    Walk recursively over a list of objects and convert a tree into a list 
    having "in" and  "out" (and maybe "flat") nesting descriptors.
    
    """
    if result is None: result = [] 
    result.append("in")
    for object in input_list:
        result.append(object)
        if object.child_categories.values():
            child_list = object.child_categories.iterator()
            item_list = _generate_item_list(child_list, result=result)
            for item in item_list:
                if item not in result:
                    result.append(item)
        # else:
            # result.append("flat")

    result.append("out")
    return result
    
def _generate_category_list():
    """
    Generates a list of dictionaries representing a categories tree structure.
    The core functionality is into _generate_category_list function.
    Each dictionary contains a template action and an object required to
    execute that action.
    In order to work properly this function requires a category tree
    root having a name property 'invisible_root_category'.
    
    """
    root = Category.objects.get(name='invisible_root_category')
    level_one_branches = Category.active.filter(parent_categories=root)
    simple_list = _generate_item_list(level_one_branches)
    simple_list = simple_list[1:-1]
    result = []
    max_index = len(simple_list) - 1 
    for index, item in enumerate(simple_list):
        if index != max_index and simple_list[index+1] == "in":
            continue
        elif item == "in":
            result.append({'action':'open_nested_menu', 'object': simple_list[index - 1]})
        elif item == "out":
            result.append({'action':'close_nested_menu', 'object': None })
        else:
            result.append({'action':'add_menu_item', 'object': item })
    return  result
    
