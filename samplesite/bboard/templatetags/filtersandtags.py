from django import template
from django.utils.safestring import mark_safe   # to add some html tags

register = template.Library()


# 1
# @register.filter(name='cur')            
@register.filter(is_safe=True)            # this filter will be allowed in template
def currency(value, name='руб.'):
    return mark_safe(f'{value} <strong>{name}</strong>')

# register.filter('currency', currency)     # The same as decorator

# 2
@register.simple_tag
def lst(sep, *args):
    return mark_safe(f'{sep.join(args)} (Итого <strong>{len(args)}</strong>)')

# 3
@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}