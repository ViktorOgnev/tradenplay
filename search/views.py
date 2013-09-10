from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf
from django.utils.translation import ugettext_lazy as _

from tradenplay.settings import PAGINATE_BY

from search import search_utils


def results(request, template_name="search/results.html"):
    context = {}
    # Get current search phrase.
    q = request.GET.get('q', '')
    # Get current page number. Set to 1 if missing or invalid.
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    # Retrieve the matching items
    matching_items = search_utils.products(q).get('products')
    # Generate the paginator object.
    paginator = Paginator(matching_items, PAGINATE_BY)
    context['paginator'] = paginator
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
    context['results'] = results
    # Store the search.
    search_utils.store(request, q)
    # Report back with corresp title.
    # " TODO: Test this one thoroughly for Unicode issues"
    page_title = ''.join([str(_("Search results for")), q])  
    context.update(csrf(request))
    return render_to_response(
                              template_name,
                              context,
                              context_instance=RequestContext(request)
                             )
                                
        
    