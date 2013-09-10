from django import template

register = template.Library()

@register.inclusion_tag("tags/form_table_row.html")
def form_table_row(form_field):
    return {'form_field': form_field }

@register.inclusion_tag("tags/invite_to_login.html")
def invite_to_login(request):
    return {'request': request }
