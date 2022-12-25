from django import template


register = template.Library()

@register.filter
def index(value, i):
    try:
        ret_val =  value[int(i)]
    except IndexError:
        ret_val = None
    return ret_val
        

