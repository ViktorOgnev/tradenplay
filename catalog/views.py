from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from endless_pagination.decorators import page_template

from tagging.models import Tag, TaggedItem
from tagging.utils import LOGARITHMIC

from cart import cart_utils
from stats import stat_utils
from tradenplay.settings import PRODUCTS_PER_ROW, CACHE_TIMEOUT

from .models import Category, Product, ProductReview, HomepageSeoText
from .forms import ProductAddToCartForm, ProductReviewForm


def index(request, template_name="catalog/index.html"):
    context = {}
    context["search_recs"] = stat_utils.recommended_from_search(request)
    context["featured"] = Product.featured.values()[0:PRODUCTS_PER_ROW]
    context["recently_viewed"] = stat_utils.get_recently_viewed(request)
    context["view_recs"] = stat_utils.recommend_from_views(request)
    context["page_title"] = _('Tradenplay.com - the best place \
                              to trade your music stuff')
    bestsellers = Product.active.values().filter(is_bestseller=True)
    context["bestsellers"] = []
    for i, item in enumerate(bestsellers):
        if i % 6 == 0:
            context["bestsellers"].append([])
        context["bestsellers"][-1].append(item)

    context["seo_text"] = HomepageSeoText.objects.get(pk=1).seo_text

    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def show_category(request, slug, template_name="catalog/category.html"):
    context = {}
    category_cache_key = request.path
    category = cache.get(category_cache_key)
    if not category:
        category = get_object_or_404(Category.active, slug=slug)
        cache.set(category_cache_key, category, CACHE_TIMEOUT)
    context['category'] = category
    context['child_categories'] = category.child_categories.values()
    context['products'] = category.product_set.values().filter(is_active=True)
    context['page_title'] = category.name
    context['meta_keywords'] = category.meta_keywords
    context['meta_description'] = category.meta_description
    context['filter_groups'] = []
    for filter_group in category.filter_groups.all():
        group = {'name': filter_group.name, 'filters': []}
        for filter in filter_group.filters.all():
            group['filters'].append(filter.name)
        context['filter_groups'].append(group)
    list_of_id_dicts = context['products'].values("id")
    context['product_ids'] = [id_dict.values()[0]
                              for id_dict in list_of_id_dicts]
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))

# New product view with get/post detection
# It could be a good idea to rewrite it later as a class based view


@page_template('catalog/reviews_page.html')
def show_product(request,
                 slug,
                 template_name="catalog/product.html",
                 extra_context=None
                 ):
    product_cache_key = request.path
    product = cache.get(product_cache_key)

    if not product:
        product = get_object_or_404(Product.active.all(), slug=slug)
        if not product:
            raise SyntaxError("cannot get a product")
        cache.set(product_cache_key, product, CACHE_TIMEOUT)
    elif not product.is_active:
        raise Http404
    context = {}
    context['product'] = product
    stat_utils.log_product_view(request, product)

    context['categories'] = product.categories.all()
    context['page_title'] = product.name
    context['meta_keywords'] = product.meta_keywords
    context['meta_description'] = product.meta_description

    # What's the method?
    if request.method == 'POST':
        # Add the bound form to cart_create
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # Check if posted data is valid
        if form.is_valid():
            # Add to cart and redirect to cart page
            cart_utils.add_to_cart(request)
            # If test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(reverse('show_cart'))

    else:
        # It's a get, create and unbound form. Note request is a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # Assign a hidden input to a product slug
    form.fields['slug'].widget.attrs['value'] = slug
    context['form'] = form
    # Set the test cookie on a first GET request
    request.session.set_test_cookie()

    context['product_reviews'] = ProductReview.approved.filter(
        product=product).order_by('-date')
    context['review_form'] = ProductReviewForm()

    if extra_context is not None:
        context.update(extra_context)

    context.update(csrf(request))

    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def ajax_filter_products(request):

    
    filters_unicode = request.GET.get('filters', '')
    ids_unicode = request.GET.get('product_ids', '')
    
    ids_list = [int(i) for i in ids_unicode[1:-1].replace(' ', '').split(',')]
    already_filtered = Product.active.filter(id__in=ids_list)
    if filters_unicode == u'':
        filtered_product_list = already_filtered 
    else:
        filters_list = [filter for filter in filters_unicode.split(',')]
        filtered_product_list = []
        for product in already_filtered:
            for filter in filters_list:
                if filter not in [name_dict.values()[0]
                              for name_dict in product.specifications.values("name")]:
                    break
            else:
                filtered_product_list.append(product)

        
    template = 'tags/product_list.html'    
    html = render_to_string(template, {'products': filtered_product_list})
    json_response = simplejson.dumps({'success': 'True', 'html': html})
    return HttpResponse(json_response, content_type="application/javascript")



@login_required
def add_review(request):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        slug = request.POST.get('id_slug')
        product = Product.active.get(slug=slug)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            template = "catalog/product_review.html"
            html = render_to_string(template, {'review': review})
            json_response = simplejson.dumps({'success': 'True', 'html': html})

        else:
            html = form.errors.as_ul()
            json_response = simplejson.dumps(
                {'success': 'False', 'html': html})

        if request.is_ajax():
            return HttpResponse(json_response,
                                content_type="application/javascript")
        else:
            return HttpResponseRedirect(product.get_absolute_url())


@login_required
def add_tag(request):

    tags = request.POST.get('id_tag', '')
    slug = request.POST.get('id_slug', '')
    if len(tags) > 2:
        product = Product.active.get(slug=slug)
        html = u''
        template_name = 'catalog/tag_link.html'
        for tag in tags.split():
            tag.strip(',')
            Tag.objects.add_tag(product, tag)
        for tag in product.tags:
            html += render_to_string(template_name, {'tag': tag})
        json_response = simplejson.dumps({'success': 'True', 'html': html})
    else:
        json_response = simplejson.dumps({'success': 'False'})

    if request.is_ajax():
        return HttpResponse(json_response,
                            content_type='application/javascript; charset=utf-8')
    else:
        return HttpResponseRedirect(product.get_absolute_url())


def tag_cloud(request, template_name="catalog/tag_cloud"):
    context = {}
    context['product_tags'] = Tag.objects.cloud_for_model(
        Product,
        steps=9,
        distribution=LOGARITHMIC,
        filters={'is_active': True}
    )
    context['page_title'] = _("Product tag cloud")
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def tag(request, tag, template_name="catalog/tag.html"):
    context = {}
    context['tag'] = tag
    context['products'] = TaggedItem.objects.get_by_model(Product.active, tag)
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def autocomplete_products(request):
    term = request.GET.get('term', '')
    products = Product.active.values("name").filter(name__istartswith=term)
    product_list = [product["name"] for product in products]
    json_response = simplejson.dumps(product_list)
    return HttpResponse(json_response,
                        content_type='application/javascript; charset=utf-8')
