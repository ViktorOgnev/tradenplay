import os
import base64

from django.contrib.auth.models import User

from search.models import SearchTerm
from tradenplay.settings import PRODUCTS_PER_ROW
from catalog.models import Product

from .models import ProductView


def get_tracking_id(request):
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']


def recommended_from_search(request):
    """
    Collects up to PRODUCTS_PER_ROW recomendations for crosselling according
    to user's search history.
    """
    common_words = frequent_search_words(request)
    from search import search_utils
    matching = []
    for word in common_words:
        results = search_utils.products(word).get('products', [])
        for result in results:
            if len(matching) < PRODCUTS_PER_ROW and not result in matching:
                matching.append(result)
    return matching


def frequent_search_words(request):
    # Get the ten most recent searches from the database.
    searches = SearchTerm.objects.filter(
        tracking_id=get_tracking_id(request)).values('q').order_by('-search_date')[0:10]
    # Join all of the searches together into a single string.
    search_string = ''.join([search['q'] for search in searches])
    # return the top three most common words in the searches.
    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(text):
    words = text.split()
    # Assing a rank to each word based on frequency.
    ranked_words = [(word, words.count(word)) for word in set(words)]
    sorted_words = sorted(ranked_words, key=(lambda word: -word[1]))
    # Return the list of words, most frequent first.
    return [p[0] for p in sorted_words]


def log_product_view(request, product):
    tracking_id = get_tracking_id(request)
    try:
        view = ProductView.objects.get(
            tracking_id=tracking_id, product=product)
        view.save()

    except ProductView.DoesNotExist:
        view = ProductView()
        view.product = product
        view.ip_address = request.META.get('REMOTE_ADDR')
        if not request.META.get('REMOTE_ADDR'):
            view.ip_address = '127.0.0.1'
        view.tracking_id = tracking_id
        if request.user.is_authenticated():
            view.user = request.user

        view.save()


def recommend_from_views(request):
    tracking_id = get_tracking_id(request)
    # Get recently viewed products.
    viewed = get_recently_viewed(request)

    # If there are previously vewed products, get other tracking id that have
    # viewed those products.
    if viewed:
        product_views = ProductView.objects.filter(
            product__in=viewed).values('tracking_id')
        tracking_ids = [view['tracking_id'] for view in product_views]

        # If there are other  tracking ids, get other products
        if tracking_ids:
            all_viewed = Product.active.filter(
                productview__tracking_id__in=tracking_ids)

            # If there are other products, get them, excluding the products
            # that the customer has already viewed
            if all_viewed is not None:
                other_viewed = ProductView.objects.filter(
                    product__in=all_viewed).exclude(product__in=viewed)

                if other_viewed:
                    return Product.active.filter(productview__in=other_viewed).distinct()


def get_recently_viewed(request):
    tracking_id = get_tracking_id(request)
    product_views = ProductView.objects.filter(tracking_id=tracking_id).values(
        'product_id').order_by('-date')[0:PRODUCTS_PER_ROW]
    product_ids = [view['product_id'] for view in product_views]
    return Product.active.filter(id__in=product_ids)
