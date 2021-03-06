from django.db.models import Q

from catalog.models import Product
from search.models import SearchTerm
from stats import stat_utils

STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not', 'of',
               'on', 'or', 'that', 'the', 'to', 'with']


def store(request, q):
    """
    Store the search text in the database, so that a further research could be
    made.
    """
    # If search text is longer than 3 characters, store it in the DB
    # " TODO: An obvious reimplementation of saving constraints required"
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        # term.tracking_id = stat_utils.get_tracking_id(request)
        term.user = None
        if request.user.is_authenticated():
            term.user = request.user
        # "TODO: serious security isssue. Injection possible. Fix!!"
        term.save()


def products(search_text):
    """ get products matching the search text """
    words = _prepare_words(search_text)
    products = Product.active.all()
    results = {}
    for word in words:
        products = products.filter(Q(name__icontains=word) |
                                   Q(description__icontains=word) |
                                   Q(sku__iexact=word) |
                                   Q(brand__icontains=word) |
                                   Q(meta_description__icontains=word) |
                                   Q(meta_keywords__icontains=word))
        results['products'] = products
    return results


def _prepare_words(text):
    words = text.split()
    for common_word in STRIP_WORDS:
        if common_word in words:
            words.remove(common)
    return words[0:5]
