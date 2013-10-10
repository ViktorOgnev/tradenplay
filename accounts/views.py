from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import urlresolvers, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson

from checkout.models import Order, OrderItem

from .forms import UserProfileForm, RegistrationForm
from accounts import profile


def register(request, template_name="registration/register.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = RegistrationForm(postdata)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = postdata.get('email', '')
            user.save()
            username = postdata.get('username', '')
            password = postdata.get('password1', '')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=username, password=password)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
    page_title = _("User registration")
    context = locals()
    context.update(csrf(request))
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@login_required
def my_account(request, template_name="registration/my_account.html"):
    page_title = _("My account")
    # import pdb; pdb.set_trace()
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


@login_required
def order_details(request, order_id, template_name="registration/order_details.html"):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = _("Order details for order number %s") % (order.number)
    order_items = OrderItem.objects.filter(order=order)
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


@login_required
def order_info(request, template_name="registration/order_info.html"):
    if request.method == "POST":
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserProfileForm(instance=user_profile)
    page_title = _("Edit order information")
    context = locals()
    context.update(csrf(request))
    return render_to_resonse(template_name, context,
                             context_instance=RequestContext(request))

def log_out(request):
        
    template_name = "registration/auth_box.html"
    html = render_to_string(template_name)
    json_response = simplejson.dumps({'success': 'True', 'html': html})
       
    if request.is_ajax():
        logout(request)
        return HttpResponse(json_response, 
                            content_type='application/javascript; charset=utf-8')
    # else:
        # url = request.path
        # logout(request)
        # return HttpResponseRedirect(url)
def log_in(request):
    
    context = {}
    next = reverse('catalog_home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            error = None
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    error = _("Account is disabled")
            else:
                error = _("Sorry, we were unable to acceept this login/password")
            if request.is_ajax():
                if error is None:
                    html = render_to_string("registration/auth_box.html")
                    response = {'success':'True', 'html': html}
                else:
                    response = {'success': 'False', 'error': error}
                json_response = simplejson.dumps(response)
                return HttpResponse(json_response,
                            content_type='application/javascript; charset=utf-8')
            #If it's a nonajax request - just redirect to a previous page
            else:
                HttpResponseRedirect(next)
    # GET
    else:
        form = AuthenticationForm()                                                                                                                                        
    
    context.update({'next': next,                                                                                                
                    'login_form': form,                                                                                                                         
                    'request': request,                                                                                                                  
                   })
    
    if request.is_ajax():
        try:
            html = render_to_string("registration/login_form.html", context)
            json_response = simplejson.dumps({'success': 'True', 'html': html})
            return HttpResponse(json_response,
                                content_type='application/javascript; charset=utf-8')
        except Exception, e:
            
            json_response = simplejson.dumps({'success': 'True', 'html': e})
            return HttpResponse(json_response,
                                content_type='application/javascript; charset=utf-8')
    else:
        return HttpResponseRedirect(next)
            
def ajax_login(request):
    try:
        request.POST[u'login']
        dictionary = request.POST
    except:
        dictionary = request.GET
    user = authenticate(username = dictionary[u'login'], password = dictionary[u'password'])    
    if user and user.is_active:
        login(request, user)
        result = True
    else:
        result = False
    response = HttpResponse(json.dumps(result), mimetype = u'application/json')
    return response