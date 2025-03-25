from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def getattribute(obj, attr):
    """
    Obtém um atributo de um objeto dinamicamente a partir de uma string.
    """
    if hasattr(obj, attr):
        value = getattr(obj, attr)
        if callable(value):
            try:
                value = value()
            except:
                value = None
        return value
    elif hasattr(obj, 'get_%s_display' % attr):
        return getattr(obj, 'get_%s_display' % attr)()
    return None
