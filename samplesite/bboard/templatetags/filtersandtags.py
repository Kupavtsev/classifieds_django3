from locale import currency
from django import template

register = template.Library()


# @register.filter(name='cur')            
@register.filter()            # this filter will be allowed in template
def currency(value, name='руб.'):
    return f'{value} {name}'

# register.filter('currency', currency)     # The same as decorator