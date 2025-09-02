from django import template

register = template.Library()

@register.filter(name="get_item")
def get_item(mapping, key):
    try:
        return mapping.get(key, "")
    except AttributeError:
        return ""
