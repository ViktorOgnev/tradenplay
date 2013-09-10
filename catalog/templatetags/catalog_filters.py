from django import template
import locale

register = template.Library()


@register.filter(name='currency')
def currency(value):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL, '')
    loc = locale.localeconv()
    value = value if value else 0

    return locale.currency(value, loc['currency_symbol'], grouping=True)
